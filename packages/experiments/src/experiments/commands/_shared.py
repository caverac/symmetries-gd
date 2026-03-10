"""Shared helpers for validity-assessment commands."""

from __future__ import annotations

import numpy as np
from symmetries import PotentialConfig, compare_variances, compute_invariants
from symmetries._types import InvariantResult, VarianceComparison


def run_single_simulation(
    config: PotentialConfig,
    n_particles: int,
    r_min: float,
    r_max: float,
    t_end: float,
    n_steps: int,
    seed: int,
) -> tuple[InvariantResult, VarianceComparison]:
    """Generate ICs, integrate orbits, and return invariant + variance data.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration for the simulation.
    n_particles : int
        Number of test particles.
    r_min : float
        Minimum initial cylindrical radius.
    r_max : float
        Maximum initial cylindrical radius.
    t_end : float
        Integration end time.
    n_steps : int
        Number of time steps.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    tuple[InvariantResult, VarianceComparison]
        Computed invariants and their variance comparison.
    """
    rng = np.random.default_rng(seed)

    r_cyl = rng.uniform(r_min, r_max, size=n_particles)
    vr = np.zeros(n_particles)

    # Compute circular velocity for Hernquist bulge + MN disk + NFW halo
    # Hernquist: v_c^2 = M * R / (R + a)^2
    v_b_sq = config.bulge_mass * r_cyl / (r_cyl + config.bulge_scale) ** 2
    # Miyamoto-Nagai in the midplane (z=0): v_c^2 = M * R^2 / (R^2 + (a+b)^2)^1.5
    ab = config.disk_a + config.disk_b
    v_d_sq = config.disk_mass * r_cyl**2 / (r_cyl**2 + ab**2) ** 1.5
    # NFW: v_c^2 = M * [ln(1+R/a) - R/(R+a)] / R  (galpy uses amp as total mass proxy)
    x = r_cyl / config.halo_a
    v_h_sq = config.halo_amp * (np.log(1.0 + x) - x / (1.0 + x)) / r_cyl
    vt = np.sqrt(v_b_sq + v_d_sq + v_h_sq)

    z = np.zeros(n_particles)
    vz = np.zeros(n_particles)
    phi = rng.uniform(0, 2 * np.pi, size=n_particles)

    times = np.linspace(0.0, t_end, n_steps)

    result = compute_invariants(config, r_cyl, vr, vt, z, vz, phi, times)
    comparison = compare_variances(result)

    return result, comparison
