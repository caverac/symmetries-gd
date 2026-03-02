"""Stress test: sweep bar_strength and track C_2 / J_R variance."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from experiments._console import console
from experiments._constants import (
    DEFAULT_DELTA,
    DEFAULT_N_PARTICLES,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_STRESS_BAR_MAX,
    DEFAULT_STRESS_BAR_MIN,
    DEFAULT_STRESS_N_POINTS,
    DEFAULT_T_END,
)
from experiments._plotting import configure_axes, docs_figure
from experiments.commands._shared import run_single_simulation
from matplotlib.figure import Figure
from symmetries import PotentialConfig


@docs_figure("stress-test.png")
def _build_figure(bar_strengths: np.ndarray, median_var_c2: np.ndarray, median_var_jr: np.ndarray) -> Figure:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    configure_axes(ax, log=True)

    ax.plot(bar_strengths, median_var_c2, "o-", label=r"$C_2$")
    ax.plot(bar_strengths, median_var_jr, "s--", label=r"$J_R$")

    ax.set_xlabel("Bar strength")
    ax.set_ylabel("Median variance")
    ax.legend(frameon=False)

    return fig


@click.command("stress-test")
@click.option("-n", "--n-particles", type=int, default=DEFAULT_N_PARTICLES, show_default=True, help="Particles.")
@click.option("--bar-min", type=float, default=DEFAULT_STRESS_BAR_MIN, show_default=True, help="Min bar strength.")
@click.option("--bar-max", type=float, default=DEFAULT_STRESS_BAR_MAX, show_default=True, help="Max bar strength.")
@click.option("--n-points", type=int, default=DEFAULT_STRESS_N_POINTS, show_default=True, help="Sweep points.")
@click.option("--r-min", type=float, default=DEFAULT_R_MIN, show_default=True, help="Min initial radius (kpc).")
@click.option("--r-max", type=float, default=DEFAULT_R_MAX, show_default=True, help="Max initial radius (kpc).")
@click.option("--t-end", type=float, default=DEFAULT_T_END, show_default=True, help="Integration end time (Gyr).")
@click.option("--n-steps", type=int, default=DEFAULT_N_STEPS, show_default=True, help="Number of time steps.")
@click.option("--delta", type=float, default=DEFAULT_DELTA, show_default=True, help="Staeckel delta parameter.")
@click.option("--seed", type=int, default=DEFAULT_SEED, show_default=True, help="Random seed.")
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    show_default=True,
    help="Output directory for NPZ file.",
)
def stress_test(
    n_particles: int,
    bar_min: float,
    bar_max: float,
    n_points: int,
    r_min: float,
    r_max: float,
    t_end: float,
    n_steps: int,
    delta: float,
    seed: int,
    output_dir: Path,
) -> None:
    """Stress test: sweep bar_strength and track variance."""
    bar_strengths = np.logspace(np.log10(bar_min), np.log10(bar_max), n_points)
    median_var_c2 = np.empty(n_points)
    median_var_jr = np.empty(n_points)

    for i, bs in enumerate(bar_strengths):
        console.print(f"[bold]bar_strength={bs:.4f} ({i + 1}/{n_points})[/bold]")
        config = PotentialConfig(bar_strength=float(bs))
        _, comp = run_single_simulation(config, n_particles, r_min, r_max, t_end, n_steps, delta, seed)
        median_var_c2[i] = float(np.median(comp.var_c2))
        median_var_jr[i] = float(np.median(comp.var_jr))

    _build_figure(bar_strengths, median_var_c2, median_var_jr)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "stress-test.npz"

    np.savez(
        out_path,
        bar_strengths=bar_strengths,
        median_var_c2=median_var_c2,
        median_var_jr=median_var_jr,
        n_particles=np.array(n_particles),
        n_points=np.array(n_points),
    )

    console.print(f"Saved: {out_path}")
