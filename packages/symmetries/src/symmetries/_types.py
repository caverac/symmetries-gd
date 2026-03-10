"""Immutable data containers for the symmetries package."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import numpy as np
from numpy.typing import NDArray


@runtime_checkable
class GalpyPotential(Protocol):
    """Structural protocol for galpy potential instances.

    Captures the minimal interface used by our code and by galpy's
    module-level helpers (``vcirc``, ``Orbit.integrate``, action-angle
    finders).
    """

    def __call__(self, R: float, z: float, phi: float = ..., t: float = ...) -> float:  # pylint: disable=invalid-name
        """Evaluate the potential at (R, z, phi, t)."""

    def Rforce(self, R: float, z: float, phi: float = ..., t: float = ...) -> float:  # pylint: disable=invalid-name
        """Evaluate the radial force at (R, z, phi, t)."""


@dataclass(frozen=True, slots=True)
class PotentialConfig:
    """Configuration for the composite galactic potential.

    Three-component axisymmetric model (Hernquist bulge + Miyamoto-Nagai disk
    + NFW halo) plus an optional rotating Dehnen bar perturbation.

    Default values produce a Milky-Way-like rotation curve with
    ``V_circ ~ 1`` from ``R = 0.5`` to ``R = 2`` in galpy natural units
    (``R_0 = 8`` kpc, ``V_0 = 220`` km/s).

    Parameters
    ----------
    bulge_mass : float
        Amplitude of the Hernquist bulge potential (galpy natural units).
    bulge_scale : float
        Scale radius of the Hernquist sphere (0.5 kpc / 8 kpc).
    disk_mass : float
        Amplitude of the Miyamoto-Nagai disk.
    disk_a : float
        Disk scale length (3 kpc / 8 kpc).
    disk_b : float
        Disk scale height (0.28 kpc / 8 kpc).
    halo_amp : float
        Amplitude of the NFW halo.
    halo_a : float
        NFW scale radius (16 kpc / 8 kpc).
    bar_strength : float
        Bar strength parameter Af for the Dehnen bar potential.
    bar_scale : float
        Bar radius rb (4 kpc / 8 kpc).
    bar_tform : float
        Bar formation time (galpy natural units, negative = past).
    bar_tsteady : float
        Time for bar to reach full strength (galpy natural units).
    bar_pattern_speed : float
        Bar pattern speed (40 km/s/kpc in natural units).
    """

    bulge_mass: float = 0.17
    bulge_scale: float = 0.0625
    disk_mass: float = 0.9
    disk_a: float = 0.375
    disk_b: float = 0.035
    halo_amp: float = 3.5
    halo_a: float = 2.0
    bar_strength: float = 0.15
    bar_scale: float = 0.5
    bar_tform: float = 0.0
    bar_tsteady: float = 28.0
    bar_pattern_speed: float = 1.45


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
    jz : NDArray[np.floating]
        Vertical action values with shape ``(n_particles, n_times)``.
    jr : NDArray[np.floating]
        Radial action values with shape ``(n_particles, n_times)``.
    l_sq : NDArray[np.floating]
        Total angular momentum squared with shape ``(n_particles, n_times)``.
    time : NDArray[np.floating]
        Time array with shape ``(n_times,)``.
    phase : PhasePoint
        Phase-space data used for computation.
    """

    jz: NDArray[np.floating]
    jr: NDArray[np.floating]
    l_sq: NDArray[np.floating]
    time: NDArray[np.floating]
    phase: PhasePoint


@dataclass(frozen=True, slots=True)
class VarianceComparison:
    """Variance comparison between J_z and J_R.

    Parameters
    ----------
    var_jz : NDArray[np.floating]
        Temporal variance of J_z per particle, shape ``(n_particles,)``.
    var_jr : NDArray[np.floating]
        Temporal variance of J_R per particle, shape ``(n_particles,)``.
    var_l_sq : NDArray[np.floating]
        Temporal variance of L^2 per particle, shape ``(n_particles,)``.
    ratio : NDArray[np.floating]
        Element-wise ``Var(J_z) / Var(J_R)``, shape ``(n_particles,)``.
    median_ratio : float
        Median of the ratio across all particles.
    """

    var_jz: NDArray[np.floating]
    var_jr: NDArray[np.floating]
    var_l_sq: NDArray[np.floating]
    ratio: NDArray[np.floating]
    median_ratio: float = field(default=0.0)


@dataclass(frozen=True, slots=True)
class PopulationConfig:
    """Configuration for a stellar population used in DF-based sampling.

    Parameters
    ----------
    n_particles : int
        Number of particles to sample.
    hr : float
        Radial scale length of the quasi-isothermal DF.
    sr : float
        Radial velocity dispersion at the solar radius.
    sz : float
        Vertical velocity dispersion at the solar radius.
    hsr : float
        Radial scale length of the radial velocity dispersion.
    hsz : float
        Radial scale length of the vertical velocity dispersion.
    r_min : float
        Minimum cylindrical radius for sampling.
    r_max : float
        Maximum cylindrical radius for sampling.
    z_max : float
        Maximum height for vertical rejection sampling (natural units).
        Default 0.05 (~ 400 pc).
    label : str
        Human-readable label for this population.
    """

    n_particles: int
    hr: float
    sr: float
    sz: float
    hsr: float
    hsz: float
    r_min: float
    r_max: float
    z_max: float = 0.05
    label: str = ""


@dataclass(frozen=True, slots=True)
class InitialConditionsConfig:
    """Configuration for DF-based initial condition sampling.

    Parameters
    ----------
    populations : tuple[PopulationConfig, ...]
        Tuple of population configurations to sample.
    seed : int
        Random seed for reproducibility.
    """

    populations: tuple[PopulationConfig, ...] = field(default_factory=tuple)
    seed: int = 42
