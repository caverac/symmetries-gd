r"""Deformed Casimir invariant C_2 = L^2 + Tr(Q_tilde^2) / omega^2.

Interpolates between the Kepler SO(4) and harmonic SU(3) Casimirs
using the sigmoid-weighted generalized tensor Q_ij.
Pure NumPy -- no galpy.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from symmetries.tensors import angular_momentum_squared, sigmoid, tensor_trace_squared


def compute_c2(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mu: float,
    plummer_mass: float,
    plummer_scale: float,
    mass: float = 1.0,
) -> NDArray[np.floating]:
    r"""Compute the deformed Casimir invariant.

    .. math::
        C_2 = L^2 + \frac{\mathrm{Tr}(\tilde{Q}^2)}{\omega^2}

    where :math:`Q_{ij} = p_i p_j / (2m) + (\Psi/2)\, x_i x_j` uses
    the virial convention (factor 1/2 on Psi) so that Q reduces to the
    Fradkin tensor T in the harmonic limit, giving :math:`C_2 \to C_H`.

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
    r_core = mu * plummer_scale / plummer_mass
    omega = np.sqrt(plummer_mass / plummer_scale**3)

    l_sq = angular_momentum_squared(pos, vel)

    r = np.sqrt(np.sum(pos**2, axis=-1))
    r_safe = np.maximum(r, 1e-30)

    sigma = sigmoid(r, r_core)
    psi = (1.0 - sigma) * (mu / r_safe**3) + sigma * omega**2

    mom = mass * vel
    kinetic = np.einsum("...i,...j->...ij", mom, mom) / (2.0 * mass)
    pos_outer = np.einsum("...i,...j->...ij", pos, pos)
    q = kinetic + (psi / 2.0)[..., np.newaxis, np.newaxis] * pos_outer

    tr_q = np.einsum("...ii->...", q)
    identity = np.eye(3)
    q_tilde = q - (tr_q[..., np.newaxis, np.newaxis] / 3.0) * identity

    tr_q_tilde_sq = tensor_trace_squared(q_tilde)

    return l_sq + tr_q_tilde_sq / omega**2  # type: ignore[no-any-return]
