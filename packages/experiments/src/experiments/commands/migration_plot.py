"""Three-panel time-trace plot: R_g, J_z, J_R for three selected particles."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import click
import matplotlib.pyplot as plt
import numpy as np
from experiments._console import console
from experiments._constants import R0_KPC, TIME_UNIT_GYR
from experiments._plotting import configure_axes, docs_figure, paper_style
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray


@docs_figure("migration-traces.png")
def _build_figure(
    time_gyr: NDArray[np.floating],
    rg_kpc: NDArray[np.floating],
    jz: NDArray[np.floating],
    jr: NDArray[np.floating],
    labels: list[str],
) -> Figure:
    """Build the three-panel migration figure.

    Parameters
    ----------
    time_gyr : ndarray
        Time array in Gyr, shape ``(n_times,)``.
    rg_kpc : ndarray
        Guiding radius in kpc for selected particles, shape ``(3, n_times)``.
    jz : ndarray
        J_z for selected particles, shape ``(3, n_times)``.
    jr : ndarray
        J_R for selected particles, shape ``(3, n_times)``.
    labels : list[str]
        Legend labels for the three particles.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    colors = ["#1a1a1a", "#4f4f4f", "#303030"]
    linestyles = ["-", "--", "-."]
    fig: Figure
    axes: tuple[Axes, Axes, Axes]

    with plt.rc_context(paper_style()):
        fig, axes = plt.subplots(3, 1, figsize=(4.5, 7), sharex=True)

        for i in range(3):
            axes[0].plot(time_gyr, rg_kpc[i], color=colors[i], lw=2, linestyle=linestyles[i])
            axes[1].plot(time_gyr, jz[i], color=colors[i], lw=2, linestyle=linestyles[i], label=labels[i])
            axes[2].plot(time_gyr, jr[i], color=colors[i], lw=2, linestyle=linestyles[i])

        axes[0].set_ylabel(r"$R_g$ (kpc)")
        axes[1].legend(frameon=False, loc="upper left")
        axes[1].set_ylabel(r"$J_z$")
        axes[2].set_ylabel(r"$J_R$")
        axes[2].set_xlabel("Time (Gyr)")

        for ax in axes:
            configure_axes(ax)

        fig.align_ylabels(axes)
        fig.tight_layout(h_pad=0.4)

    return fig


def _pick_particles(
    rg: NDArray[np.floating],
    r_target: float = 0.9,
    band: float = 0.15,
) -> tuple[int, int, int]:
    """Select three particles starting near the same radius.

    Restricts to particles with initial R_g within ``r_target +/- band``,
    then picks non-migrating, outward, and inward migrators from that subset.

    Parameters
    ----------
    rg : ndarray
        Guiding radius, shape ``(n_particles, n_times)``.
    r_target : float
        Target initial guiding radius (natural units). Default 0.8 (~6.4 kpc).
    band : float
        Half-width of the radial band (natural units). Default 0.15 (~1.2 kpc).

    Returns
    -------
    tuple[int, int, int]
        Indices of the three selected particles.
    """
    rg0 = rg[:, 0]
    in_band = np.where(np.abs(rg0 - r_target) < band)[0]
    if len(in_band) < 3:
        in_band = np.arange(len(rg0))

    # Non-migrator: smallest temporal standard deviation (truly constant Rg)
    rg_std = np.std(rg[in_band], axis=1)
    i_stay = in_band[int(np.argmin(rg_std))]
    # Outward/inward: largest endpoint change, excluding the non-migrator
    remaining = in_band[in_band != i_stay]
    dr_remaining = rg[remaining, -1] - rg[remaining, 0]
    i_out = remaining[int(np.argmax(dr_remaining))]
    i_in = remaining[int(np.argmin(dr_remaining))]
    return i_stay, i_out, i_in


@click.command("migration-plot")
@click.option("--name", required=True, help="Run name in the database.")
@click.option(
    "--db",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("packages/experiments/data/simulations.db"),
    show_default=True,
    help="Path to the simulations database.",
)
def migration_plot(name: str, db: Path) -> None:
    """Three-panel plot: R_g, J_z, J_R for migrating and non-migrating stars."""
    conn = sqlite3.connect(str(db))
    row = conn.execute("SELECT id FROM runs WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise click.ClickException(f"Run '{name}' not found in {db}.")
    run_id: int = row[0]

    rows = conn.execute(
        "SELECT particle_idx, time, jr, jz, guiding_radius "
        "FROM snapshots WHERE run_id = ? ORDER BY particle_idx, time",
        (run_id,),
    ).fetchall()
    conn.close()

    data = np.array(rows)
    pids = np.unique(data[:, 0].astype(int))
    n_times = len(np.unique(data[:, 1]))
    n_p = len(pids)

    times = np.unique(data[:, 1])
    jr = data[:, 2].reshape(n_p, n_times)
    jz = data[:, 3].reshape(n_p, n_times)
    rg = data[:, 4].reshape(n_p, n_times)

    # Exclude particles with any sentinel J_R
    good = ~(jr >= 9000).any(axis=1)
    jr = jr[good]
    jz = jz[good]
    rg = rg[good]

    i_stay, i_out, i_in = _pick_particles(rg)
    idx = [i_stay, i_out, i_in]
    labels = ["Non-migrating", "Outward migrator", "Inward migrator"]

    dr_kpc = (rg[idx, -1] - rg[idx, 0]) * R0_KPC
    console.print(f"Particles: {int(good.sum())}/{n_p} (sentinel-free)")
    console.print(f"Selected: stay={i_stay}, out={i_out}, in={i_in}")
    console.print(f"  dRg (kpc): stay={dr_kpc[0]:.1f}, out={dr_kpc[1]:.1f}, in={dr_kpc[2]:.1f}")

    _build_figure(
        times * TIME_UNIT_GYR,
        rg[idx] * R0_KPC,
        jz[idx],
        jr[idx],
        labels,
    )
