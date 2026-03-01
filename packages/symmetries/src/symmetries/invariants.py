"""Deformed Casimir invariant C_2(lambda) computation.

Combines angular momentum and the generalized symmetry tensor to
produce the quasi-conserved integral of motion.  Pure NumPy --no galpy.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from symmetries.tensors import angular_momentum_squared, generalized_tensor, tensor_trace_squared


def compute_c2(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    r_core: float,
    mu: float,
    omega: float,
    mass: float = 1.0,
) -> NDArray[np.floating]:
    r"""Compute the deformed action C_2(lambda).

    .. math::
        C_2(\lambda) = L^2 + \mathrm{Tr}(Q_{ij} Q^{ij})

    With alpha = beta = 1 for the initial proof-of-concept.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.
    r_core : float
        Core radius defining the SO(4)-SU(3) transition scale.
    mu : float
        Gravitational parameter GM.
    omega : float
        Harmonic frequency of the bulge potential.
    mass : float
        Particle mass (default 1.0 for test particles).

    Returns
    -------
    NDArray
        Deformed action values, shape ``(...)``.
    """
    l_sq = angular_momentum_squared(pos, vel)
    q_tensor = generalized_tensor(pos, vel, r_core, mu, omega, mass)
    tr_q_sq = tensor_trace_squared(q_tensor)
    return l_sq + tr_q_sq
