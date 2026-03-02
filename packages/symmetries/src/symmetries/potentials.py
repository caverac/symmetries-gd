"""Galpy potential construction for the composite galactic model.

Builds the three-component potential: Keplerian SMBH + Plummer bulge +
rotating Dehnen bar.  This is one of only two modules that import galpy.
"""

from __future__ import annotations

from typing import Any

from galpy.potential import DehnenBarPotential, KeplerPotential, PlummerPotential
from symmetries._types import PotentialConfig


def build_kepler(config: PotentialConfig) -> Any:
    """Build a Keplerian point-mass potential for the SMBH.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with ``smbh_mass``.

    Returns
    -------
    KeplerPotential
        The galpy Kepler potential instance.
    """
    return KeplerPotential(amp=config.smbh_mass)


def build_plummer(config: PotentialConfig) -> Any:
    """Build a Plummer sphere potential for the stellar bulge.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with ``plummer_mass`` and ``plummer_scale``.

    Returns
    -------
    PlummerPotential
        The galpy Plummer potential instance.
    """
    return PlummerPotential(amp=config.plummer_mass, b=config.plummer_scale)


def build_bar(config: PotentialConfig) -> Any:
    """Build a rotating Dehnen bar potential.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration with bar parameters.

    Returns
    -------
    DehnenBarPotential
        The galpy Dehnen bar potential instance.
    """
    return DehnenBarPotential(
        Af=config.bar_strength,
        rb=config.bar_scale,
        tform=config.bar_tform,
        tsteady=config.bar_tsteady,
        omegab=config.bar_pattern_speed,
    )


def build_axisymmetric(config: PotentialConfig) -> list[Any]:
    """Build the axisymmetric part of the potential (Kepler + Plummer).

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration.

    Returns
    -------
    list
        List of galpy potential instances ``[kepler, plummer]``.
    """
    return [build_kepler(config), build_plummer(config)]


def build_composite(config: PotentialConfig) -> list[Any]:
    """Build the full three-component galactic potential.

    Parameters
    ----------
    config : PotentialConfig
        Full potential configuration.

    Returns
    -------
    list
        List of galpy potential instances ``[kepler, plummer, bar]``.
    """
    return [*build_axisymmetric(config), build_bar(config)]
