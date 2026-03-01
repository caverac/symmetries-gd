"""Immutable data containers for the symmetries package."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class PotentialConfig:
    """Configuration for the composite galactic potential.

    Parameters
    ----------
    smbh_mass : float
        Mass of the supermassive black hole in solar masses.
    plummer_mass : float
        Mass of the Plummer bulge in solar masses.
    plummer_scale : float
        Scale radius of the Plummer sphere in kpc.
    bar_mass : float
        Mass of the Dehnen bar in solar masses.
    bar_scale : float
        Scale length of the bar in kpc.
    bar_tform : float
        Bar formation time in Gyr.
    bar_tsteady : float
        Time for bar to reach full strength in Gyr.
    bar_pattern_speed : float
        Bar pattern speed in km/s/kpc.
    """

    smbh_mass: float = 4e6
    plummer_mass: float = 1e10
    plummer_scale: float = 0.5
    bar_mass: float = 1e9
    bar_scale: float = 1.0
    bar_tform: float = -5.0
    bar_tsteady: float = 2.0
    bar_pattern_speed: float = 40.0


@dataclass(frozen=True, slots=True)
class PhasePoint:
    """Phase-space state for an ensemble of particles at multiple time steps.

    Parameters
    ----------
    pos : NDArray[np.floating]
        Positions with shape ``(n_particles, n_times, 3)``.
    vel : NDArray[np.floating]
        Velocities with shape ``(n_particles, n_times, 3)``.
    time : NDArray[np.floating]
        Time array with shape ``(n_times,)``.
    """

    pos: NDArray[np.floating]
    vel: NDArray[np.floating]
    time: NDArray[np.floating]


@dataclass(frozen=True, slots=True)
class InvariantResult:
    """Results from invariant computation across an orbit ensemble.

    Parameters
    ----------
    c2 : NDArray[np.floating]
        Deformed action values with shape ``(n_particles, n_times)``.
    jr : NDArray[np.floating]
        Radial action values with shape ``(n_particles, n_times)``.
    time : NDArray[np.floating]
        Time array with shape ``(n_times,)``.
    phase : PhasePoint
        Phase-space data used for computation.
    """

    c2: NDArray[np.floating]
    jr: NDArray[np.floating]
    time: NDArray[np.floating]
    phase: PhasePoint


@dataclass(frozen=True, slots=True)
class VarianceComparison:
    """Variance comparison between C_2 and J_R.

    Parameters
    ----------
    var_c2 : NDArray[np.floating]
        Temporal variance of C_2 per particle, shape ``(n_particles,)``.
    var_jr : NDArray[np.floating]
        Temporal variance of J_R per particle, shape ``(n_particles,)``.
    ratio : NDArray[np.floating]
        Element-wise ``Var(C_2) / Var(J_R)``, shape ``(n_particles,)``.
    median_ratio : float
        Median of the ratio across all particles.
    """

    var_c2: NDArray[np.floating]
    var_jr: NDArray[np.floating]
    ratio: NDArray[np.floating]
    median_ratio: float = field(default=0.0)
