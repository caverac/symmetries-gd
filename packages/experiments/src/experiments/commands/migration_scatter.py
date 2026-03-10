"""Generate the migration scatter plot from a simulation run."""

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


@docs_figure("migration-scatter.png")
def _build_figure(
    rg0_kpc: NDArray[np.floating],
    ln_ratio: NDArray[np.floating],
    r_cr_kpc: float,
) -> Figure:
    """Build the migration scatter plot.

    Parameters
    ----------
    rg0_kpc : ndarray
        Initial guiding radius in kpc.
    ln_ratio : ndarray
        ln(R_g,final / R_g,initial).
    r_cr_kpc : float
        Corotation radius in kpc.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    with plt.rc_context(paper_style()):
        fig, ax = plt.subplots(figsize=(4.5, 4.0))

        ax.scatter(rg0_kpc, ln_ratio, alpha=0.7, s=4, edgecolors="black", linewidths=0.3, color="black")
        ax.axhline(0, color="black", linestyle="--", linewidth=2)
        ax.axvline(r_cr_kpc, color="gray", linestyle="--", linewidth=0.8)
        ax.text(
            r_cr_kpc,
            0.98,
            r"$R_{\mathrm{CR}}$",
            va="top",
            ha="right",
            rotation=90,
            transform=ax.get_xaxis_transform(),
        )

        ax.set_xlabel(r"$R_{g,0}$ (kpc)")
        ax.set_ylabel(r"$\ln(R_g \,/\, R_{g,0})$")
        ax.set_xlim(left=0, right=10)
        ax.set_ylim(-3, 3)
        configure_axes(ax)

    return fig


@click.command("migration-scatter")
@click.option("--name", required=True, help="Run name in the database.")
@click.option(
    "--db",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("packages/experiments/data/simulations.db"),
    show_default=True,
    help="Path to the simulations database.",
)
def migration_scatter(name: str, db: Path) -> None:
    """Scatter plot: ln(R_g / R_g,0) vs R_g,0."""
    conn = sqlite3.connect(str(db))
    row = conn.execute(
        "SELECT id, bar_pattern_speed FROM runs WHERE name = ?",
        (name,),
    ).fetchone()
    if row is None:
        raise click.ClickException(f"Run '{name}' not found in {db}.")
    run_id: int = row[0]
    bar_pattern_speed: float = row[1]

    rows = conn.execute(
        "SELECT particle_idx, time, guiding_radius FROM snapshots WHERE run_id = ? ORDER BY particle_idx, time",
        (run_id,),
    ).fetchall()
    conn.close()

    data = np.array(rows)
    pids = np.unique(data[:, 0].astype(int))
    n_times = len(np.unique(data[:, 1]))
    n_p = len(pids)

    rg = data[:, 2].reshape(n_p, n_times)
    rg0 = rg[:, 0]
    rg_end = rg[:, -1]

    good = rg0 > 1e-10
    rg0 = rg0[good]
    rg_end = rg_end[good]

    rg0_kpc = rg0 * R0_KPC
    ln_ratio = np.log(rg_end / rg0)

    r_cr_kpc = R0_KPC / bar_pattern_speed
    _build_figure(rg0_kpc, ln_ratio, r_cr_kpc)

    console.print(f"Particles: {int(good.sum())}/{n_p}")
    console.print(f"Max |ln(Rg/Rg0)|: {float(np.max(np.abs(ln_ratio))):.3f}")
    console.print(f"Median |dRg|: {float(np.median(np.abs(rg_end - rg0))) * R0_KPC:.2f} kpc")
