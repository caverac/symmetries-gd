"""Galpy potential construction for the composite galactic model.

Builds the four-component potential: Keplerian SMBH + Plummer bulge +
Miyamoto-Nagai disk + rotating Dehnen bar.
"""

from __future__ import annotations

from galpy.potential import DehnenBarPotential, KeplerPotential, MiyamotoNagaiPotential, PlummerPotential
from symmetries._types import GalpyPotential, PotentialConfig


def build_kepler(config: PotentialConfig) -> GalpyPotential:
    """Build a Keplerian point-mass potential for the SMBH.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with ``smbh_mass``.

    Returns
    -------
    GalpyPotential
        The galpy Kepler potential instance.
    """
    return KeplerPotential(amp=config.smbh_mass)  # type: ignore[no-any-return]


def build_plummer(config: PotentialConfig) -> GalpyPotential:
    """Build a Plummer sphere potential for the stellar bulge.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with ``plummer_mass`` and ``plummer_scale``.

    Returns
    -------
    GalpyPotential
        The galpy Plummer potential instance.
    """
    return PlummerPotential(amp=config.plummer_mass, b=config.plummer_scale)  # type: ignore[no-any-return]


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
        List of galpy potential instances ``[kepler, plummer, disk]``.
    """
    return [build_kepler(config), build_plummer(config), build_disk(config)]


def build_composite(config: PotentialConfig) -> list[GalpyPotential]:
    """Build the full four-component galactic potential.

    Parameters
    ----------
    config : PotentialConfig
        Full potential configuration.

    Returns
    -------
    list[GalpyPotential]
        List of galpy potential instances ``[kepler, plummer, disk, bar]``.
    """
    return [*build_axisymmetric(config), build_bar(config)]
