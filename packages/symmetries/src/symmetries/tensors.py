"""Tensor algebra for dynamical symmetry deformation.

Implements the Laplace-Runge-Lenz tensor, Fradkin tensor, and the
parameterized interpolation between SO(4) and SU(3) symmetry limits.
All functions are pure NumPy --no galpy dependency.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def angular_momentum_squared(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Compute squared angular momentum L^2 = |r x v|^2.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.

    Returns
    -------
    NDArray
        Squared angular momentum, shape ``(...)``.
    """
    cross = np.cross(pos, vel)
    return np.sum(cross**2, axis=-1)  # type: ignore[no-any-return]


def lrl_vector(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mu: float,
) -> NDArray[np.floating]:
    """Compute the Laplace-Runge-Lenz vector A = v x L - mu * r_hat.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.
    mu : float
        Gravitational parameter GM.

    Returns
    -------
    NDArray
        LRL vector, shape ``(..., 3)``.
    """
    ang_mom = np.cross(pos, vel)
    v_cross_l = np.cross(vel, ang_mom)
    r = np.sqrt(np.sum(pos**2, axis=-1, keepdims=True))
    r_hat = pos / np.maximum(r, 1e-30)
    return v_cross_l - mu * r_hat  # type: ignore[no-any-return]


def lrl_tensor(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mu: float,
) -> NDArray[np.floating]:
    """Compute the rank-2 LRL tensor A_ij = A_i * A_j.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.
    mu : float
        Gravitational parameter GM.

    Returns
    -------
    NDArray
        LRL tensor, shape ``(..., 3, 3)``.
    """
    a_vec = lrl_vector(pos, vel, mu)
    return np.einsum("...i,...j->...ij", a_vec, a_vec)  # type: ignore[no-any-return]


def fradkin_tensor(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    omega: float,
    mass: float,
) -> NDArray[np.floating]:
    """Compute the Fradkin tensor T_ij = p_i*p_j/(2m) + m*omega^2*r_i*r_j/2.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.
    omega : float
        Harmonic oscillator frequency.
    mass : float
        Particle mass.

    Returns
    -------
    NDArray
        Fradkin tensor, shape ``(..., 3, 3)``.
    """
    mom = mass * vel
    kinetic = np.einsum("...i,...j->...ij", mom, mom) / (2.0 * mass)
    potential = 0.5 * mass * omega**2 * np.einsum("...i,...j->...ij", pos, pos)
    return kinetic + potential  # type: ignore[no-any-return]


def psi_function(
    r: NDArray[np.floating],
    r_core: float,
    mu: float,
    omega: float,
) -> NDArray[np.floating]:
    r"""Compute the structural function Psi for the generalized tensor.

    Interpolates between the Keplerian (mu/r^3) and harmonic (omega^2)
    limits using a sigmoid centered at r = r_core.

    Parameters
    ----------
    r : NDArray
        Radial distances, shape ``(...)``.
    r_core : float
        Core radius defining the transition scale.
    mu : float
        Gravitational parameter GM.
    omega : float
        Harmonic frequency.

    Returns
    -------
    NDArray
        Structural function values, shape ``(...)``.
    """
    lam = r / r_core
    sigma = 1.0 / (1.0 + np.exp(-4.0 * (lam - 1.0)))
    r_safe = np.maximum(r, 1e-30)
    kepler_part = mu / r_safe**3
    harmonic_part = omega**2
    return (1.0 - sigma) * kepler_part + sigma * harmonic_part  # type: ignore[no-any-return]


def phi_function(
    r: NDArray[np.floating],
    r_core: float,
    mu: float,
) -> NDArray[np.floating]:
    r"""Compute the structural function Phi for the generalized tensor.

    The scalar offset vanishes in the harmonic limit (Phi -> 0)
    and equals -mu/r in the Keplerian limit.

    Parameters
    ----------
    r : NDArray
        Radial distances, shape ``(...)``.
    r_core : float
        Core radius defining the transition scale.
    mu : float
        Gravitational parameter GM.

    Returns
    -------
    NDArray
        Structural function values, shape ``(...)``.
    """
    lam = r / r_core
    sigma = 1.0 / (1.0 + np.exp(-4.0 * (lam - 1.0)))
    r_safe = np.maximum(r, 1e-30)
    return (1.0 - sigma) * (-mu / r_safe)  # type: ignore[no-any-return]


def generalized_tensor(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    r_core: float,
    mu: float,
    omega: float,
    mass: float = 1.0,
) -> NDArray[np.floating]:
    r"""Compute the generalized symmetry tensor Q_ij(lambda).

    .. math::
        Q_{ij}(\lambda) = \frac{p_i p_j}{2m}
                        + \Psi(r,\lambda)\, x_i x_j
                        + \Phi(r,\lambda)\, \delta_{ij}

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.
    r_core : float
        Core radius defining the transition scale.
    mu : float
        Gravitational parameter GM.
    omega : float
        Harmonic frequency.
    mass : float
        Particle mass (default 1.0 for test particles).

    Returns
    -------
    NDArray
        Generalized tensor, shape ``(..., 3, 3)``.
    """
    mom = mass * vel
    kinetic = np.einsum("...i,...j->...ij", mom, mom) / (2.0 * mass)

    r = np.sqrt(np.sum(pos**2, axis=-1))
    psi = psi_function(r, r_core, mu, omega)
    phi = phi_function(r, r_core, mu)

    pos_outer = np.einsum("...i,...j->...ij", pos, pos)
    psi_expanded = psi[..., np.newaxis, np.newaxis]
    spatial = psi_expanded * pos_outer

    phi_expanded = phi[..., np.newaxis, np.newaxis]
    identity = np.eye(3)
    scalar = phi_expanded * identity

    return kinetic + spatial + scalar  # type: ignore[no-any-return]


def tensor_trace_squared(tensor: NDArray[np.floating]) -> NDArray[np.floating]:
    r"""Compute Tr(Q^2) = Q_ij * Q_ji.

    Parameters
    ----------
    tensor : NDArray
        Symmetric tensor, shape ``(..., 3, 3)``.

    Returns
    -------
    NDArray
        Trace of the squared tensor, shape ``(...)``.
    """
    return np.einsum("...ij,...ji->...", tensor, tensor)  # type: ignore[no-any-return]
