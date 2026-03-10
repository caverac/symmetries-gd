r"""Staeckel focal distance and angular momentum computation.

Provides the Staeckel-derived focal distance :math:`\Delta(R)` for a
Miyamoto-Nagai disk potential, derived from the Staeckel separability
condition (Sanders 2012, Binney 2012).

The focal distance acts as a "gauge field" that encodes the local symmetry
of the potential, deforming from spherical (:math:`\Delta \to 0`) in the
bulge to flattened (:math:`\Delta > 0`) in the disk.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def delta_miyamoto_nagai(
    r_cyl: NDArray[np.floating],
    a: float,
    b: float,
) -> NDArray[np.floating]:
    r"""Compute the Staeckel focal distance for a Miyamoto-Nagai potential.

    Derived from the Staeckel separability condition evaluated at the
    midplane (:math:`z = 0`):

    .. math::
        \Delta^2(R) = \frac{4\,a\,(R^2 + (a + b)^2)}{3\,(a + b)} - R^2

    Parameters
    ----------
    r_cyl : NDArray
        Cylindrical radius, shape ``(...)``.
    a : float
        Disk scale length.
    b : float
        Disk scale height.

    Returns
    -------
    NDArray
        Focal distance :math:`\Delta(R)`, shape ``(...)``.
        Clipped to zero where the formula yields negative values.
    """
    ab = a + b
    delta_sq = 4.0 * a * (r_cyl**2 + ab**2) / (3.0 * ab) - r_cyl**2
    return np.sqrt(np.maximum(delta_sq, 0.0))


def angular_momentum_squared(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
) -> NDArray[np.floating]:
    r"""Compute squared angular momentum :math:`L^2 = |\mathbf{r} \times \mathbf{v}|^2`.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.

    Returns
    -------
    NDArray
        :math:`L^2`, shape ``(...)``.
    """
    cross = np.cross(pos, vel)
    return np.sum(cross**2, axis=-1)  # type: ignore[no-any-return]


def compute_l_squared(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
) -> NDArray[np.floating]:
    r"""Compute the total angular momentum squared :math:`|\mathbf{r} \times \mathbf{v}|^2`.

    Parameters
    ----------
    pos : NDArray
        Position vectors, shape ``(..., 3)``.
    vel : NDArray
        Velocity vectors, shape ``(..., 3)``.

    Returns
    -------
    NDArray
        :math:`L^2`, shape ``(...)``.
    """
    return angular_momentum_squared(pos, vel)
