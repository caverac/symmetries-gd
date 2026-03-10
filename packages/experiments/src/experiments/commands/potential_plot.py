"""Generate a circular-velocity profile of the composite galactic potential."""

from __future__ import annotations

import click
import matplotlib.pyplot as plt
import numpy as np
from experiments._console import console
from experiments._constants import R0_KPC, V0_KMS
from experiments._models import RunConfig
from experiments._plotting import configure_axes, docs_figure, paper_style
from galpy.potential import vcirc
from matplotlib.figure import Figure
from numpy.typing import NDArray
from symmetries.potentials import build_axisymmetric


@docs_figure("potential-profile.png")
def _build_figure(
    radii: NDArray[np.floating],
    vc_bulge: NDArray[np.floating],
    vc_disk: NDArray[np.floating],
    vc_halo: NDArray[np.floating],
    vc_total: NDArray[np.floating],
) -> Figure:
    """Build the circular-velocity profile figure.

    Parameters
    ----------
    radii : ndarray
        Cylindrical radii in kpc.
    vc_bulge : ndarray
        Circular velocity from the Hernquist bulge in km/s.
    vc_disk : ndarray
        Circular velocity from the Miyamoto-Nagai disk in km/s.
    vc_halo : ndarray
        Circular velocity from the NFW halo in km/s.
    vc_total : ndarray
        Total circular velocity in km/s.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    with plt.rc_context(paper_style()):
        fig, ax = plt.subplots(figsize=(4.5, 4.0))

        ax.plot(radii, vc_bulge, "--", color="gray", lw=1.0, label="Bulge")
        ax.plot(radii, vc_disk, "-.", color="gray", lw=1.0, label="Disk")
        ax.plot(radii, vc_halo, ":", color="gray", lw=1.0, label="Halo")
        ax.plot(radii, vc_total, "-", color="black", lw=1.5, label="Total")

        ax.set_xlabel(r"$R$ (kpc)")
        ax.set_ylabel(r"$V_{\mathrm{circ}}(R)$ (km/s)")
        ax.set_ylim(bottom=0)
        ax.legend(frameon=False)
        configure_axes(ax)

    return fig


@click.command("potential-plot")
def potential_plot() -> None:
    """Plot the circular-velocity profile."""
    config = RunConfig(name="_plot").to_potential_config()
    bulge, disk, halo = build_axisymmetric(config)
    axisym = [bulge, disk, halo]

    radii = np.linspace(0.05, 20.0 / R0_KPC, 300)

    vc_bulge = np.array([float(vcirc(bulge, r)) for r in radii])
    vc_disk = np.array([float(vcirc(disk, r)) for r in radii])
    vc_halo = np.array([float(vcirc(halo, r)) for r in radii])
    vc_total = np.array([float(vcirc(axisym, r)) for r in radii])

    _build_figure(
        radii * R0_KPC,
        vc_bulge * V0_KMS,
        vc_disk * V0_KMS,
        vc_halo * V0_KMS,
        vc_total * V0_KMS,
    )
    console.print("[green]Done.[/green]")
