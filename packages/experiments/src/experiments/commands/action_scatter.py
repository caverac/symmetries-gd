"""Generate the action-stability scatter plot from a simulation run."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import click
import matplotlib.pyplot as plt
import numpy as np
from experiments._console import console
from experiments._constants import R0_KPC
from experiments._plotting import configure_axes, docs_figure, paper_style
from matplotlib.figure import Figure
from numpy.typing import NDArray

_BANDS: list[tuple[float, float, str, str]] = [
    (0.0, 3.0, "0.2", r"$R_{g,0} < 3$ kpc"),
    (3.0, 7.0, "0.5", r"$3 < R_{g,0} < 7$ kpc"),
    (7.0, 100.0, "0.8", r"$R_{g,0} > 7$ kpc"),
]


@docs_figure("action-scatter.png")
def _build_figure(
    std_jr: NDArray[np.floating],
    std_jz: NDArray[np.floating],
    rg0_kpc: NDArray[np.floating],
) -> Figure:
    """Build the action-stability scatter plot.

    Parameters
    ----------
    std_jr : ndarray
        std(J_R) / |L_z|_0 per particle.
    std_jz : ndarray
        std(J_z) / |L_z|_0 per particle.
    rg0_kpc : ndarray
        Initial guiding radius in kpc per particle.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    with plt.rc_context(paper_style()):
        fig, ax = plt.subplots(figsize=(4.5, 4.0))

        for lo, hi, gray, label in _BANDS:
            mask = (rg0_kpc >= lo) & (rg0_kpc < hi)
            if not mask.any():
                continue
            ax.scatter(
                std_jr[mask],
                std_jz[mask],
                color=gray,
                edgecolors="none",
                s=8,
                label=label,
            )

        ax.plot([-2, 2], [-2, 2], "k-", lw=1.5)
        ax.set_xlim(-0.01, 0.5)
        ax.set_ylim(-0.01, 0.5)
        ax.set_xlabel(r"$\sigma(J_R)\;/\;|L_{z,0}|$")
        ax.set_ylabel(r"$\sigma(J_z)\;/\;|L_{z,0}|$")
        ax.legend(frameon=False)
        configure_axes(ax)

    return fig


@click.command("action-scatter")
@click.option("--name", required=True, help="Run name in the database.")
@click.option(
    "--db",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("packages/experiments/data/simulations.db"),
    show_default=True,
    help="Path to the simulations database.",
)
def action_scatter(name: str, db: Path) -> None:
    """Scatter plot: |Delta Jz/Lz| vs |Delta Jr/Lz|, coloured by Delta Rg."""
    conn = sqlite3.connect(str(db))
    row = conn.execute("SELECT id FROM runs WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise click.ClickException(f"Run '{name}' not found in {db}.")
    run_id: int = row[0]

    rows = conn.execute(
        "SELECT particle_idx, time, jr, jz, guiding_radius, lz "
        "FROM snapshots WHERE run_id = ? ORDER BY particle_idx, time",
        (run_id,),
    ).fetchall()
    conn.close()

    data = np.array(rows)
    pids = np.unique(data[:, 0].astype(int))
    n_times = len(np.unique(data[:, 1]))
    n_p = len(pids)

    jr = data[:, 2].reshape(n_p, n_times)
    jz = data[:, 3].reshape(n_p, n_times)
    rg = data[:, 4].reshape(n_p, n_times)
    lz = data[:, 5].reshape(n_p, n_times)

    lz0 = np.abs(lz[:, 0])
    good = ~(jr >= 9000).any(axis=1) & (lz0 > 1e-10)
    n_kept = int(good.sum())

    jr = jr[good]
    jz = jz[good]
    rg = rg[good]
    lz0 = lz0[good]

    std_jr_norm = np.std(jr, axis=1) / lz0
    std_jz_norm = np.std(jz, axis=1) / lz0
    rg0_kpc = rg[:, 0] * R0_KPC

    _build_figure(std_jr_norm, std_jz_norm, rg0_kpc)

    med_jz = float(np.median(std_jz_norm))
    med_jr = float(np.median(std_jr_norm))
    console.print(f"Particles: {n_kept}/{n_p}")
    console.print(f"Median std(Jz)/|Lz|: {med_jz:.2e}")
    console.print(f"Median std(Jr)/|Lz|: {med_jr:.2e}")
    console.print(f"Ratio: {med_jz / med_jr:.2e}")
