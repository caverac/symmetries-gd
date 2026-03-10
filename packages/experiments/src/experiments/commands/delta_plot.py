r"""Generate a plot of the Staeckel focal distance :math:`\Delta(R)`."""

from __future__ import annotations

import click
import matplotlib.pyplot as plt
import numpy as np
from experiments._console import console
from experiments._constants import R0_KPC
from experiments._models import RunConfig
from experiments._plotting import configure_axes, docs_figure, paper_style
from matplotlib.figure import Figure
from numpy.typing import NDArray
from symmetries.invariants import delta_miyamoto_nagai


@docs_figure("delta-profile.png")
def _build_figure(
    radii: NDArray[np.floating],
    delta: NDArray[np.floating],
    bulge_scale: float,
    disk_a: float,
) -> Figure:
    r"""Build the :math:`\Delta(R)` profile figure.

    Parameters
    ----------
    radii : ndarray
        Radial distances in kpc.
    delta : ndarray
        Staeckel focal distance at each radius in kpc.
    bulge_scale : float
        Hernquist bulge scale radius in kpc.
    disk_a : float
        Disk scale length in kpc.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    with plt.rc_context(paper_style()):
        fig, ax = plt.subplots(figsize=(4.5, 4.0))

        ax.plot(radii, delta, "-", color="black", lw=1.5)

        ax.axvline(bulge_scale, color="gray", ls="--", lw=0.8)
        ax.axvline(disk_a, color="gray", ls="--", lw=0.8)

        ax.text(
            bulge_scale,
            0.02,
            r"$a_b$",
            va="bottom",
            ha="right",
            rotation=90,
            transform=ax.get_xaxis_transform(),
        )
        ax.text(
            disk_a,
            0.02,
            r"$a_d$",
            va="bottom",
            ha="right",
            rotation=90,
            transform=ax.get_xaxis_transform(),
        )

        ax.set_xlabel(r"$R$ (kpc)")
        ax.set_ylabel(r"$\Delta(R)$ (kpc)")
        configure_axes(ax)

    return fig


@click.command("delta-plot")
def delta_plot() -> None:
    r"""Plot the Staeckel focal distance :math:`\Delta(R)`."""
    config = RunConfig(name="_plot").to_potential_config()

    radii = np.logspace(np.log10(0.01), np.log10(10.0 / R0_KPC), 500)
    delta = delta_miyamoto_nagai(radii, config.disk_a, config.disk_b)

    _build_figure(radii * R0_KPC, delta * R0_KPC, config.bulge_scale * R0_KPC, config.disk_a * R0_KPC)
    console.print("[green]Done.[/green]")
