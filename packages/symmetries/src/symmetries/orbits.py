"""Orbit integration and action computation via galpy.

This is one of only two modules that import galpy.  It accepts cylindrical
initial conditions, integrates orbits, extracts Cartesian phase-space
coordinates, and computes actions.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from galpy.actionAngle import actionAngleStaeckel
from galpy.orbit import Orbit
from numpy.typing import NDArray
from symmetries._types import PhasePoint


def cartesian_to_cylindrical(
    pos: NDArray[np.floating],
    vel: NDArray[np.floating],
) -> tuple[
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
]:
    """Convert Cartesian (x,y,z,vx,vy,vz) to cylindrical (R,vR,vT,z,vz,phi).

    Parameters
    ----------
    pos : NDArray
        Cartesian positions, shape ``(..., 3)``.
    vel : NDArray
        Cartesian velocities, shape ``(..., 3)``.

    Returns
    -------
    tuple
        ``(R, vR, vT, z, vz, phi)`` arrays, each with shape ``(...)``.
    """
    x, y, z = pos[..., 0], pos[..., 1], pos[..., 2]
    vx, vy, vz = vel[..., 0], vel[..., 1], vel[..., 2]

    r_cyl = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)

    r_safe = np.maximum(r_cyl, 1e-30)
    cos_phi = x / r_safe
    sin_phi = y / r_safe

    v_r = vx * cos_phi + vy * sin_phi
    v_t = -vx * sin_phi + vy * cos_phi

    return r_cyl, v_r, v_t, z, vz, phi


def integrate_orbits(
    r_cyl: NDArray[np.floating],
    vr: NDArray[np.floating],
    vt: NDArray[np.floating],
    z: NDArray[np.floating],
    vz: NDArray[np.floating],
    phi: NDArray[np.floating],
    potential: Any,
    times: NDArray[np.floating],
) -> PhasePoint:
    """Integrate orbits in the given potential and return Cartesian phase space.

    Parameters
    ----------
    r_cyl : NDArray
        Cylindrical radii, shape ``(n_particles,)``.
    vr : NDArray
        Radial velocities, shape ``(n_particles,)``.
    vt : NDArray
        Tangential velocities, shape ``(n_particles,)``.
    z : NDArray
        Vertical positions, shape ``(n_particles,)``.
    vz : NDArray
        Vertical velocities, shape ``(n_particles,)``.
    phi : NDArray
        Azimuthal angles, shape ``(n_particles,)``.
    potential : list or Potential
        Galpy potential or list of potentials.
    times : NDArray
        Integration time array, shape ``(n_times,)``.

    Returns
    -------
    PhasePoint
        Cartesian phase-space data for all particles and times.
    """
    n_particles = len(r_cyl)
    n_times = len(times)
    pos_out = np.zeros((n_particles, n_times, 3))
    vel_out = np.zeros((n_particles, n_times, 3))

    for i in range(n_particles):
        orb = Orbit(
            vxvv=[r_cyl[i], vr[i], vt[i], z[i], vz[i], phi[i]],
        )
        orb.integrate(times, potential)

        pos_out[i, :, 0] = orb.x(times)
        pos_out[i, :, 1] = orb.y(times)
        pos_out[i, :, 2] = orb.z(times)
        vel_out[i, :, 0] = orb.vx(times)
        vel_out[i, :, 1] = orb.vy(times)
        vel_out[i, :, 2] = orb.vz(times)

    return PhasePoint(pos=pos_out, vel=vel_out, time=times)


def compute_actions(
    phase: PhasePoint,
    potential: Any,
    delta: float = 0.5,
) -> NDArray[np.floating]:
    """Compute the radial action J_R for each particle at each time step.

    Parameters
    ----------
    phase : PhasePoint
        Phase-space data with shape ``(n_particles, n_times, 3)``.
    potential : list or Potential
        Galpy potential or list of potentials.
    delta : float
        Focal length for the Staeckel approximation.

    Returns
    -------
    NDArray
        Radial action values, shape ``(n_particles, n_times)``.
    """
    aa = actionAngleStaeckel(pot=potential, delta=delta)
    n_particles, n_times, _ = phase.pos.shape
    jr_out = np.zeros((n_particles, n_times))

    for i in range(n_particles):
        for t in range(n_times):
            pos_t = phase.pos[i, t]
            vel_t = phase.vel[i, t]
            r_cyl, v_r, v_t, z_val, vz_val, phi = cartesian_to_cylindrical(pos_t, vel_t)
            orb = Orbit(vxvv=[float(r_cyl), float(v_r), float(v_t), float(z_val), float(vz_val), float(phi)])
            jr_val, _, _ = aa(orb)
            jr_out[i, t] = np.asarray(jr_val).flat[0]

    return jr_out
