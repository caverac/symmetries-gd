"""Convergence check: sweep bar_tform and track C_2 / J_R variance."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from experiments._console import console
from experiments._constants import (
    DEFAULT_CONV_N_POINTS,
    DEFAULT_CONV_TFORM_MAX,
    DEFAULT_CONV_TFORM_MIN,
    DEFAULT_DELTA,
    DEFAULT_N_PARTICLES,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_T_END,
)
from experiments._plotting import configure_axes, docs_figure
from experiments.commands._shared import run_single_simulation
from matplotlib.figure import Figure
from symmetries import PotentialConfig


@docs_figure("convergence.png")
def _build_figure(tform_values: np.ndarray, median_var_c2: np.ndarray, median_var_jr: np.ndarray) -> Figure:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    configure_axes(ax)
    ax.set_yscale("log")

    ax.plot(tform_values, median_var_c2, "o-", label=r"$C_2$")
    ax.plot(tform_values, median_var_jr, "s--", label=r"$J_R$")

    ax.set_xlabel(r"$t_\mathrm{form}$")
    ax.set_ylabel("Median variance")
    ax.legend(frameon=False)

    return fig


@click.command("convergence")
@click.option("-n", "--n-particles", type=int, default=DEFAULT_N_PARTICLES, show_default=True, help="Particles.")
@click.option("--tform-min", type=float, default=DEFAULT_CONV_TFORM_MIN, show_default=True, help="Min tform.")
@click.option("--tform-max", type=float, default=DEFAULT_CONV_TFORM_MAX, show_default=True, help="Max tform.")
@click.option("--n-points", type=int, default=DEFAULT_CONV_N_POINTS, show_default=True, help="Sweep points.")
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
def convergence(
    n_particles: int,
    tform_min: float,
    tform_max: float,
    n_points: int,
    r_min: float,
    r_max: float,
    t_end: float,
    n_steps: int,
    delta: float,
    seed: int,
    output_dir: Path,
) -> None:
    """Convergence check: sweep bar_tform and track variance."""
    tform_values = np.linspace(tform_min, tform_max, n_points)
    median_var_c2 = np.empty(n_points)
    median_var_jr = np.empty(n_points)

    for i, tf in enumerate(tform_values):
        console.print(f"[bold]bar_tform={tf:.2f} ({i + 1}/{n_points})[/bold]")
        config = PotentialConfig(bar_tform=float(tf))
        _, comp = run_single_simulation(config, n_particles, r_min, r_max, t_end, n_steps, delta, seed)
        median_var_c2[i] = float(np.median(comp.var_c2))
        median_var_jr[i] = float(np.median(comp.var_jr))

    _build_figure(tform_values, median_var_c2, median_var_jr)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "convergence.npz"

    np.savez(
        out_path,
        tform_values=tform_values,
        median_var_c2=median_var_c2,
        median_var_jr=median_var_jr,
        n_particles=np.array(n_particles),
        n_points=np.array(n_points),
    )

    console.print(f"Saved: {out_path}")
