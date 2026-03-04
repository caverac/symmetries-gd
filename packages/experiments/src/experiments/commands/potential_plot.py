"""Generate a radial profile of the composite galactic potential."""

from __future__ import annotations

import click
import numpy as np
from experiments._console import console
from experiments._plotting import configure_axes, docs_figure
from matplotlib.figure import Figure


@docs_figure("potential-profile.png")
def _build_figure(
    radii: np.ndarray,
    v_kepler: np.ndarray,
    v_plummer: np.ndarray,
    v_disk: np.ndarray,
    v_total: np.ndarray,
) -> Figure:
    """Build the potential profile figure.

    Parameters
    ----------
    radii : ndarray
        Cylindrical radii.
    v_kepler : ndarray
        Kepler potential evaluated at z=0.
    v_plummer : ndarray
        Plummer potential evaluated at z=0.
    v_disk : ndarray
        Miyamoto-Nagai disk potential evaluated at z=0.
    v_total : ndarray
        Total axisymmetric potential.

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 5))
    configure_axes(ax, log=False)
    ax.set_xscale("log")

    ax.plot(radii, v_kepler, "--", color="#888888", lw=1.0, label="Kepler (SMBH)")
    ax.plot(radii, v_plummer, "--", color="#5ba3cf", lw=1.0, label="Plummer (bulge)")
    ax.plot(radii, v_disk, "--", color="#8bc34a", lw=1.0, label="Miyamoto-Nagai (disk)")
    ax.plot(radii, v_total, "-", color="#1a1a1a", lw=2.0, label="Total axisymmetric")

    ax.set_xlabel(r"$R$ (natural units)")
    ax.set_ylabel(r"$\Phi(R,\, z=0)$")
    ax.legend(frameon=False, fontsize=9)

    return fig


@click.command("potential-plot")
@click.option("--smbh-mass", type=float, default=0.1, show_default=True, help="SMBH mass.")
@click.option("--plummer-mass", type=float, default=0.4, show_default=True, help="Plummer mass.")
@click.option("--plummer-scale", type=float, default=0.5, show_default=True, help="Plummer scale.")
@click.option("--disk-mass", type=float, default=0.5, show_default=True, help="Disk mass.")
@click.option("--disk-a", type=float, default=3.0, show_default=True, help="Disk scale length.")
@click.option("--disk-b", type=float, default=0.2, show_default=True, help="Disk scale height.")
def potential_plot(
    smbh_mass: float,
    plummer_mass: float,
    plummer_scale: float,
    disk_mass: float,
    disk_a: float,
    disk_b: float,
) -> None:
    """Plot the composite potential profile."""
    from galpy.potential import (
        KeplerPotential,
        MiyamotoNagaiPotential,
        PlummerPotential,
        evaluatePotentials,
    )

    kepler = KeplerPotential(amp=smbh_mass)
    plummer = PlummerPotential(amp=plummer_mass, b=plummer_scale)
    disk = MiyamotoNagaiPotential(amp=disk_mass, a=disk_a, b=disk_b)
    axisym = [kepler, plummer, disk]

    radii = np.logspace(np.log10(0.02), np.log10(10.0), 300)
    z = 0.0

    v_kepler = np.array([float(evaluatePotentials(kepler, r, z)) for r in radii])
    v_plummer = np.array([float(evaluatePotentials(plummer, r, z)) for r in radii])
    v_disk = np.array([float(evaluatePotentials(disk, r, z)) for r in radii])
    v_total = np.array([float(evaluatePotentials(axisym, r, z)) for r in radii])

    dest = _build_figure(radii, v_kepler, v_plummer, v_disk, v_total)
    console.print(f"Saved: {dest}")
