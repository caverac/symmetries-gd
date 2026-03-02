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
    delta: float,
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
    delta : float
        Staeckel delta parameter.
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

    # Compute circular velocity v_circ = sqrt(R * |dPhi/dR|)
    # For Kepler: v_c = sqrt(mu/R)
    # For Plummer: v_c = sqrt(M*R^2 / (R^2+a^2)^1.5)
    # Total v_c^2 = v_k^2 + v_p^2
    v_k_sq = config.smbh_mass / r_cyl
    v_p_sq = config.plummer_mass * r_cyl**2 / (r_cyl**2 + config.plummer_scale**2) ** 1.5
    vt = np.sqrt(v_k_sq + v_p_sq)

    z = np.zeros(n_particles)
    vz = np.zeros(n_particles)
    phi = rng.uniform(0, 2 * np.pi, size=n_particles)

    times = np.linspace(0.0, t_end, n_steps)

    result = compute_invariants(config, r_cyl, vr, vt, z, vz, phi, times, delta=delta)
    comparison = compare_variances(result)

    return result, comparison
