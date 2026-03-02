r"""Deformed Casimir invariant.

Interpolates between the Kepler SO(4) and harmonic SU(3) Casimirs
using the theoretical Lie Algebra deformation parameters Psi and Phi.
Pure NumPy -- no galpy.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from symmetries.tensors import angular_momentum_squared, phi_function, psi_function


def compute_c2(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mu: float,
    plummer_mass: float,
    plummer_scale: float,
    mass: float = 1.0,
) -> NDArray[np.floating]:
    r"""Compute the deformed Casimir invariant.

    Uses the parameterized Lie Algebra deformation operator:
    Q_ij = p_i p_j / (2m) + Psi(r) x_i x_j + Phi(r) delta_ij

    The Casimir is C2 = alpha L^2 + beta Tr(Q_tilde^2)
    where Q_tilde is the traceless part of Q.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.
    mu : float
        Gravitational parameter GM of the SMBH.
    plummer_mass : float
        Mass of the Plummer bulge.
    plummer_scale : float
        Scale radius of the Plummer sphere.
    mass : float
        Particle mass.

    Returns
    -------
    NDArray
        Deformed Casimir, shape ``(...)``.
    """
    # 1. Scaling parameters
    r_core = (mu * plummer_scale / (plummer_mass + 1e-30)) if plummer_mass > 0 else 1e30
    omega = np.sqrt(plummer_mass / (plummer_scale**3 + 1e-30))

    # 2. Base components
    l_sq = angular_momentum_squared(pos, vel)
    r = np.sqrt(np.sum(pos**2, axis=-1))

    # 3. Structural functions Psi and Phi
    # Psi(r) interpolates force-gradient: mu/r^3 -> omega^2
    # Phi(r) interpolates potential shift: -mu/r -> 0
    psi = psi_function(r, r_core, mu, omega)
    phi = phi_function(r, r_core, mu)

    # 4. Construct Symmetry Operator Q_ij
    # Q_ij = p_i p_j / (2m) + (Psi/2) x_i x_j + Phi delta_ij
    # (Virial factor 1/2 on Psi ensures Q -> T_Fradkin in Harmonic limit)
    mom = mass * vel
    kinetic = np.einsum("...i,...j->...ij", mom, mom) / (2.0 * mass)
    pos_outer = np.einsum("...i,...j->...ij", pos, pos)
    potential = (psi / 2.0)[..., np.newaxis, np.newaxis] * pos_outer

    identity = np.eye(3)
    offset = phi[..., np.newaxis, np.newaxis] * identity

    q_tensor = kinetic + potential + offset

    # 5. Extract Traceless Casimir Component
    tr_q = np.einsum("...ii->...", q_tensor)
    q_tilde = q_tensor - (tr_q[..., np.newaxis, np.newaxis] / 3.0) * identity
    tr_q_tilde_sq = np.einsum("...ij,...ji->...", q_tilde, q_tilde)

    # 6. Final Casimir sum: C2 = L^2 + Tr(Q_tilde^2) / omega_eff^2
    # In the transition, we must scale the trace term to match units of L^2.
    # The effective frequency omega_eff(r) = sqrt(Psi(r)).
    omega_eff_sq = np.maximum(psi, 1e-30)

    return l_sq + tr_q_tilde_sq / omega_eff_sq  # type: ignore[no-any-return]
