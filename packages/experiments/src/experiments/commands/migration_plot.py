"""Three-panel plot showing migration, C_2, and J_R for three particles."""

from __future__ import annotations

import click
import numpy as np
from experiments._console import console
from experiments._constants import DEFAULT_DELTA, DEFAULT_SEED
from experiments._plotting import configure_axes, docs_figure
from matplotlib.figure import Figure
from symmetries import PotentialConfig


@docs_figure("migration-traces.png")
def _build_figure(
    time: np.ndarray,
    r_guide: np.ndarray,
    c2: np.ndarray,
    jr: np.ndarray,
    labels: list[str],
) -> Figure:
    """Build the three-panel migration figure.

    Parameters
    ----------
    time : ndarray
        Time array, shape ``(n_times,)``.
    r_guide : ndarray
        Guiding radius for selected particles, shape ``(3, n_times)``.
    c2 : ndarray
        C_2 for selected particles, shape ``(3, n_times)``.
    jr : ndarray
        J_R for selected particles, shape ``(3, n_times)``.
    labels : list[str]
        Legend labels for the three particles.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    import matplotlib.pyplot as plt

    colors = ["#1a1a1a", "#e63946", "#5ba3cf"]

    fig, axes = plt.subplots(3, 1, figsize=(7, 7.5), sharex=True)

    for i in range(3):
        axes[0].plot(time, r_guide[i], color=colors[i], lw=1.2, label=labels[i])
        axes[1].plot(time, c2[i], color=colors[i], lw=1.2)
        axes[2].plot(time, jr[i], color=colors[i], lw=1.2)

    axes[0].set_ylabel(r"$R_g$ (natural units)")
    axes[0].legend(frameon=False, fontsize=9)
    axes[1].set_ylabel(r"$C_2$")
    axes[2].set_ylabel(r"$J_R$")
    axes[2].set_xlabel(r"$t$ (natural units)")

    for ax in axes:
        configure_axes(ax)

    fig.align_ylabels(axes)
    fig.tight_layout(h_pad=0.4)

    return fig


def _pick_particles(
    r_cyl: np.ndarray,
) -> tuple[int, int, int]:
    """Select three particles: non-migrating, outward, inward.

    Parameters
    ----------
    r_cyl : ndarray
        Cylindrical radius, shape ``(n_particles, n_times)``.

    Returns
    -------
    tuple[int, int, int]
        Indices of the three selected particles.
    """
    n_quarter = r_cyl.shape[1] // 4
    r_early = np.mean(r_cyl[:, :n_quarter], axis=1)
    r_late = np.mean(r_cyl[:, -n_quarter:], axis=1)
    dr = r_late - r_early

    i_stay = int(np.argmin(np.abs(dr)))
    i_out = int(np.argmax(dr))
    i_in = int(np.argmin(dr))

    return i_stay, i_out, i_in


@click.command("migration-plot")
@click.option("-n", "--n-particles", type=int, default=200, show_default=True, help="Particles.")
@click.option("--bar-strength", type=float, default=0.05, show_default=True, help="Bar strength.")
@click.option("--r-min", type=float, default=0.3, show_default=True, help="Min initial radius.")
@click.option("--r-max", type=float, default=1.5, show_default=True, help="Max initial radius.")
@click.option("--t-end", type=float, default=4.0, show_default=True, help="Integration end time.")
@click.option("--n-steps", type=int, default=300, show_default=True, help="Number of time steps.")
@click.option("--delta", type=float, default=DEFAULT_DELTA, show_default=True, help="Staeckel delta.")
@click.option("--seed", type=int, default=DEFAULT_SEED, show_default=True, help="Random seed.")
def migration_plot(
    n_particles: int,
    bar_strength: float,
    r_min: float,
    r_max: float,
    t_end: float,
    n_steps: int,
    delta: float,
    seed: int,
) -> None:
    """Three-panel plot: R_g, C_2, J_R for migrating and non-migrating stars."""
    from experiments.commands._shared import run_single_simulation

    config = PotentialConfig(bar_strength=bar_strength)

    console.print(f"[bold]Integrating {n_particles} orbits (bar_strength={bar_strength})...[/bold]")
    result, _ = run_single_simulation(config, n_particles, r_min, r_max, t_end, n_steps, delta, seed)

    # Cylindrical radius from Cartesian positions
    pos = result.phase.pos  # (n_particles, n_times, 3)
    r_cyl = np.sqrt(pos[:, :, 0] ** 2 + pos[:, :, 1] ** 2)

    # Guiding radius proxy: running mean of R over a window
    kernel = max(1, r_cyl.shape[1] // 20)
    r_guide = np.apply_along_axis(lambda m: np.convolve(m, np.ones(kernel) / kernel, mode="same"), axis=1, arr=r_cyl)

    i_stay, i_out, i_in = _pick_particles(r_cyl)
    idx = [i_stay, i_out, i_in]
    labels = ["Non-migrating", "Outward migration", "Inward migration"]

    console.print(f"Selected particles: stay={i_stay}, out={i_out}, in={i_in}")
    console.print(
        f"  R change: stay={r_guide[i_stay, -1] - r_guide[i_stay, 0]:.3f}, "
        f"out={r_guide[i_out, -1] - r_guide[i_out, 0]:.3f}, "
        f"in={r_guide[i_in, -1] - r_guide[i_in, 0]:.3f}"
    )

    dest = _build_figure(
        result.time,
        r_guide[idx],
        result.c2[idx],
        result.jr[idx],
        labels,
    )
    console.print(f"Saved: {dest}")
