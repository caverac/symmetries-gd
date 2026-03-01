"""Generate the variance-comparison figure from saved simulation data."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from experiments._console import console, err_console
from experiments._plotting import configure_axes, docs_figure
from matplotlib.figure import Figure


@docs_figure("variance-comparison.png")
def _build_figure(var_jr: np.ndarray, var_c2: np.ndarray) -> Figure:
    """Build the variance-comparison log-log scatter plot.

    Parameters
    ----------
    var_jr : ndarray
        Per-particle variance of J_R.
    var_c2 : ndarray
        Per-particle variance of C_2.

    Returns
    -------
    Figure
        Matplotlib figure ready for saving.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    configure_axes(ax, log=True)

    ax.scatter(var_jr, var_c2, s=8, alpha=0.6, edgecolors="none")

    all_vals = np.concatenate([var_jr, var_c2])
    lo, hi = float(all_vals.min()) * 0.5, float(all_vals.max()) * 2.0
    ax.plot([lo, hi], [lo, hi], "k--", lw=0.8, label="1:1")

    ax.set_xlabel(r"$\mathrm{Var}(J_R)$")
    ax.set_ylabel(r"$\mathrm{Var}(C_2)$")
    ax.legend(frameon=False)

    return fig


@click.command("variance-plot")
@click.option(
    "--data-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    required=True,
    help="Directory containing simulation.npz.",
)
def variance_plot(data_dir: Path) -> None:
    """Generate the variance-comparison figure from simulation data."""
    npz_path = data_dir / "simulation.npz"
    if not npz_path.exists():
        err_console.print(f"[red]Error:[/red] {npz_path} not found.")
        raise SystemExit(1)

    data = np.load(npz_path)
    var_jr = data["var_jr"]
    var_c2 = data["var_c2"]
    median_ratio = float(data["median_ratio"])

    dest = _build_figure(var_jr, var_c2)
    console.print(f"Saved: {dest}")
    console.print(f"Median Var(C2)/Var(JR): {median_ratio:.6e}")
