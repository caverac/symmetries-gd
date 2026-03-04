r"""Deformed Casimir invariant.

Interpolates between the Kepler SO(4) and harmonic SU(3) Casimirs
using the theoretical Lie Algebra deformation parameters Psi and Phi.
Pure NumPy -- no galpy.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from symmetries.tensors import angular_momentum_squared, sigmoid


def compute_c2(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
    mu: float,
    plummer_mass: float,
    plummer_scale: float,
    disk_mass: float = 0.0,  # pylint: disable=unused-argument
    disk_a: float = 0.0,
    mass: float = 1.0,
) -> NDArray[np.floating]:
    r"""Compute the Algebraic-Geometric Casimir.

    This invariant represents the Staeckel action calculated in a
    coordinate system whose focal distance Delta(r) deforms along the
    Lie Algebra contraction path.

    The path moves through three regimes:
    1. Spherical Core (Delta ~ 0)
    2. Ellipsoidal Bulge (Delta ~ plummer_scale)
    3. Flattened Disk (Delta ~ disk_a)

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
    disk_mass : float
        Mass of the galactic disk.
    disk_a : float
        Scale length of the disk.
    mass : float
        Particle mass.

    Returns
    -------
    NDArray
        Deformed Geometric Casimir, shape ``(...)``.
    """
    # 1. Base components
    l_sq = angular_momentum_squared(pos, vel)
    r = np.sqrt(np.sum(pos**2, axis=-1))
    pz = mass * vel[..., 2]

    # 2. Scaling parameters
    r_core = (mu * plummer_scale / (plummer_mass + 1e-30)) if plummer_mass > 0 else 1e30
    # The disk transition happens further out
    r_disk = disk_a if disk_a > 0 else 1e30

    # 3. Multi-Stage Dynamic Focal Distance Delta(r)
    # Stage 1: Kepler -> Bulge
    sig_bulge = sigmoid(r, r_core)
    # Stage 2: Bulge -> Disk
    sig_disk = sigmoid(r, r_disk)

    # Delta deforms from 0 -> plummer_scale -> disk_a
    delta_eff = (1.0 - sig_disk) * (sig_bulge * plummer_scale) + sig_disk * disk_a

    # 4. Deformed Casimir: C2 = L^2 + Delta^2 * pz^2
    return l_sq + (delta_eff**2) * (pz**2)  # type: ignore[no-any-return]
