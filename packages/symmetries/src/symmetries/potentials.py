"""Galpy potential construction for the composite galactic model.

Builds the three-component axisymmetric potential (Hernquist bulge +
Miyamoto-Nagai disk + NFW halo) plus an optional rotating Dehnen bar
perturbation.
"""

from __future__ import annotations

from galpy.potential import DehnenBarPotential, HernquistPotential, MiyamotoNagaiPotential, NFWPotential
from symmetries._types import GalpyPotential, PotentialConfig


def build_bulge(config: PotentialConfig) -> GalpyPotential:
    """Build a Hernquist sphere potential for the stellar bulge.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with ``bulge_mass`` and ``bulge_scale``.

    Returns
    -------
    GalpyPotential
        The galpy Hernquist potential instance.
    """
    return HernquistPotential(amp=config.bulge_mass, a=config.bulge_scale)  # type: ignore[no-any-return]


def build_disk(config: PotentialConfig) -> GalpyPotential:
    """Build a Miyamoto-Nagai disk potential.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with disk parameters.

    Returns
    -------
    GalpyPotential
        The galpy Miyamoto-Nagai disk instance.
    """
    return MiyamotoNagaiPotential(amp=config.disk_mass, a=config.disk_a, b=config.disk_b)  # type: ignore[no-any-return]


def build_halo(config: PotentialConfig) -> GalpyPotential:
    """Build an NFW dark matter halo potential.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with ``halo_amp`` and ``halo_a``.

    Returns
    -------
    GalpyPotential
        The galpy NFW potential instance.
    """
    return NFWPotential(amp=config.halo_amp, a=config.halo_a)  # type: ignore[no-any-return]


def build_bar(config: PotentialConfig) -> GalpyPotential:
    """Build a rotating Dehnen bar potential.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with bar parameters.

    Returns
    -------
    GalpyPotential
        The galpy Dehnen bar potential instance.
    """
    return DehnenBarPotential(  # type: ignore[no-any-return]
        Af=config.bar_strength,
        rb=config.bar_scale,
        tform=config.bar_tform,
        tsteady=config.bar_tsteady,
        omegab=config.bar_pattern_speed,
    )


def build_axisymmetric(config: PotentialConfig) -> list[GalpyPotential]:
    """Build the axisymmetric part of the potential.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration.

    Returns
    -------
    list[GalpyPotential]
        List of galpy potential instances ``[bulge, disk, halo]``.
    """
    return [build_bulge(config), build_disk(config), build_halo(config)]


def build_composite(config: PotentialConfig) -> list[GalpyPotential]:
    """Build the full galactic potential including the bar.

    Parameters
    ----------
    config : PotentialConfig
        Full potential configuration.

    Returns
    -------
    list[GalpyPotential]
        List of galpy potential instances ``[bulge, disk, halo, bar]``.
    """
    return [*build_axisymmetric(config), build_bar(config)]
