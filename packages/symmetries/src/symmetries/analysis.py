"""Pipeline orchestrator and variance comparison statistics.

Ties together potential construction, orbit integration, invariant
computation, and action calculation into a single analysis pipeline.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from symmetries._types import InvariantResult, PotentialConfig, VarianceComparison
from symmetries.invariants import compute_c2
from symmetries.orbits import compute_actions, integrate_orbits
from symmetries.potentials import build_axisymmetric, build_composite


def smbh_influence_radius(mu: float, bulge_mass: float, bulge_scale: float) -> float:
    r"""Compute the SMBH sphere-of-influence radius.

    The influence radius is where the Keplerian potential equals the
    Plummer potential: :math:`r_{\mathrm{infl}} = \mu \, a / M`.

    Parameters
    ----------
    mu : float
        SMBH gravitational parameter (mass in natural units).
    bulge_mass : float
        Mass of the Plummer bulge.
    bulge_scale : float
        Scale radius of the Plummer bulge.

    Returns
    -------
    float
        Influence radius in the same length units as *bulge_scale*.
    """
    return mu * bulge_scale / bulge_mass


def omega_from_plummer(mass: float, scale: float) -> float:
    r"""Compute the harmonic frequency from Plummer parameters.

    For a Plummer sphere the central density gives a harmonic frequency
    :math:`\omega = \sqrt{M / a^3}` (in natural units with G=1).

    Parameters
    ----------
    mass : float
        Mass of the Plummer sphere.
    scale : float
        Scale radius of the Plummer sphere.

    Returns
    -------
    float
        Harmonic frequency omega.
    """
    return float(np.sqrt(mass / scale**3))


def compute_invariants(
    config: PotentialConfig,
    r_cyl: NDArray[np.floating],
    vr: NDArray[np.floating],
    vt: NDArray[np.floating],
    z: NDArray[np.floating],
    vz: NDArray[np.floating],
    phi: NDArray[np.floating],
    times: NDArray[np.floating],
    delta: float = 0.5,
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
    delta : float
        Focal length for the Staeckel approximation.

    Returns
    -------
    InvariantResult
        Combined C_2 and J_R values for all particles and times.
    """
    potential = build_composite(config)
    axisymmetric = build_axisymmetric(config)
    phase = integrate_orbits(r_cyl, vr, vt, z, vz, phi, potential, times)

    c2 = compute_c2(
        phase.pos,
        phase.vel,
        mu=config.smbh_mass,
        plummer_mass=config.plummer_mass,
        plummer_scale=config.plummer_scale,
    )
    jr = compute_actions(phase, axisymmetric, delta=delta)

    return InvariantResult(c2=c2, jr=jr, time=times, phase=phase)


def compare_variances(result: InvariantResult) -> VarianceComparison:
    """Compute per-particle temporal variance comparison.

    Parameters
    ----------
    result : InvariantResult
        Output from :func:`compute_invariants`.

    Returns
    -------
    VarianceComparison
        Variance statistics comparing C_2 and J_R.
    """
    var_c2 = np.var(result.c2, axis=1)
    var_jr = np.var(result.jr, axis=1)
    ratio = var_c2 / np.maximum(var_jr, 1e-30)
    median_ratio = float(np.median(ratio))

    return VarianceComparison(
        var_c2=var_c2,
        var_jr=var_jr,
        ratio=ratio,
        median_ratio=median_ratio,
    )
