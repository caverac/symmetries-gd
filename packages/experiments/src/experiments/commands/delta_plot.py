"""Generate a plot of the dynamic focal distance Delta(r)."""

from __future__ import annotations

import click
import numpy as np
from experiments._console import console
from experiments._plotting import configure_axes, docs_figure
from matplotlib.figure import Figure
from symmetries.tensors import sigmoid


@docs_figure("delta-profile.png")
def _build_figure(
    radii: np.ndarray,
    delta: np.ndarray,
    r_core: float,
    r_disk: float,
    plummer_scale: float,
    disk_a: float,
) -> Figure:
    r"""Build the Delta(r) profile figure.

    Parameters
    ----------
    radii : ndarray
        Radial distances.
    delta : ndarray
        Dynamic focal distance at each radius.
    r_core : float
        SMBH influence radius (bulge transition scale).
    r_disk : float
        Disk transition scale.
    plummer_scale : float
        Plummer scale radius (bulge Delta plateau).
    disk_a : float
        Disk scale length (disk Delta plateau).

    Returns
    -------
    Figure
        Matplotlib figure.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4.5))
    configure_axes(ax, log=True)

    ax.plot(radii, delta, "-", color="#1a1a1a", lw=2.0)

    ax.axhline(plummer_scale, color="#5ba3cf", ls=":", lw=0.8, label=rf"$a_b = {plummer_scale}$")
    ax.axhline(disk_a, color="#8bc34a", ls=":", lw=0.8, label=rf"$a_d = {disk_a}$")
    ax.axvline(r_core, color="#888888", ls="--", lw=0.8, label=rf"$r_{{\mathrm{{core}}}} = {r_core:.2f}$")
    ax.axvline(r_disk, color="#8bc34a", ls="--", lw=0.8, label=rf"$r_{{\mathrm{{disk}}}} = {r_disk}$")

    ax.set_xlabel(r"$r$ (natural units)")
    ax.set_ylabel(r"$\Delta(r)$")
    ax.legend(frameon=False, fontsize=9)

    return fig


@click.command("delta-plot")
@click.option("--smbh-mass", type=float, default=0.1, show_default=True, help="SMBH mass (mu).")
@click.option("--plummer-mass", type=float, default=0.4, show_default=True, help="Plummer mass.")
@click.option("--plummer-scale", type=float, default=0.5, show_default=True, help="Plummer scale.")
@click.option("--disk-a", type=float, default=3.0, show_default=True, help="Disk scale length.")
def delta_plot(
    smbh_mass: float,
    plummer_mass: float,
    plummer_scale: float,
    disk_a: float,
) -> None:
    r"""Plot the dynamic focal distance Delta(r)."""
    r_core = smbh_mass * plummer_scale / (plummer_mass + 1e-30) if plummer_mass > 0 else 1e30
    r_disk = disk_a

    radii = np.logspace(np.log10(0.01), np.log10(15.0), 500)

    sig_bulge = sigmoid(radii, r_core)
    sig_disk = sigmoid(radii, r_disk)
    delta = (1.0 - sig_disk) * (sig_bulge * plummer_scale) + sig_disk * disk_a

    dest = _build_figure(radii, delta, r_core, r_disk, plummer_scale, disk_a)
    console.print(f"Saved: {dest}")
