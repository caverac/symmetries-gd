"""Pipeline orchestrator and variance comparison statistics.

Ties together potential construction, orbit integration, invariant
computation, and action calculation into a single analysis pipeline.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from symmetries._types import InvariantResult, PotentialConfig, VarianceComparison
from symmetries.invariants import compute_l_squared, delta_miyamoto_nagai
from symmetries.orbits import compute_actions, integrate_orbits
from symmetries.potentials import build_axisymmetric, build_composite


def compute_invariants(
    config: PotentialConfig,
    r_cyl: NDArray[np.floating],
    vr: NDArray[np.floating],
    vt: NDArray[np.floating],
    z: NDArray[np.floating],
    vz: NDArray[np.floating],
    phi: NDArray[np.floating],
    times: NDArray[np.floating],
) -> InvariantResult:
    """Run the full analysis pipeline.

    Parameters
    ----------
    config : PotentialConfig
        Potential configuration.
    r_cyl : NDArray
        Initial cylindrical radii, shape ``(n_particles,)``.
    vr : NDArray
        Initial radial velocities, shape ``(n_particles,)``.
    vt : NDArray
        Initial tangential velocities, shape ``(n_particles,)``.
    z : NDArray
        Initial vertical positions, shape ``(n_particles,)``.
    vz : NDArray
        Initial vertical velocities, shape ``(n_particles,)``.
    phi : NDArray
        Initial azimuthal angles, shape ``(n_particles,)``.
    times : NDArray
        Integration time array, shape ``(n_times,)``.

    Returns
    -------
    InvariantResult
        Combined J_z, J_R, and L^2 values for all particles and times.
    """
    potential = build_composite(config)
    axisymmetric = build_axisymmetric(config)
    phase = integrate_orbits(r_cyl, vr, vt, z, vz, phi, potential, times)

    # Staeckel focal distance from Miyamoto-Nagai derivation
    r_phase = np.sqrt(phase.pos[..., 0] ** 2 + phase.pos[..., 1] ** 2)
    delta_arr = delta_miyamoto_nagai(r_phase, config.disk_a, config.disk_b)
    # Use the median delta as the global Staeckel parameter
    delta = float(np.median(delta_arr))

    l_sq = compute_l_squared(phase.pos, phase.vel)
    jr, _lz, jz = compute_actions(phase, axisymmetric, delta=delta)

    return InvariantResult(jz=jz, jr=jr, l_sq=l_sq, time=times, phase=phase)


def compare_variances(result: InvariantResult) -> VarianceComparison:
    """Compute per-particle temporal variance comparison.

    Parameters
    ----------
    result : InvariantResult
        Output from :func:`compute_invariants`.

    Returns
    -------
    VarianceComparison
        Variance statistics comparing J_z and J_R.
    """
    var_jz = np.var(result.jz, axis=1)
    var_jr = np.var(result.jr, axis=1)
    var_l_sq = np.var(result.l_sq, axis=1)
    ratio = var_jz / np.maximum(var_jr, 1e-30)
    median_ratio = float(np.median(ratio))

    return VarianceComparison(
        var_jz=var_jz,
        var_jr=var_jr,
        var_l_sq=var_l_sq,
        ratio=ratio,
        median_ratio=median_ratio,
    )
