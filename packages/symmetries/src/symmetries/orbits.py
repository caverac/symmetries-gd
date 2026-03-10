"""Orbit integration and action computation via galpy.

Accepts cylindrical initial conditions, integrates orbits, extracts
Cartesian phase-space coordinates, and computes actions using the
Staeckel Fudge with a position-dependent focal distance.
"""

from __future__ import annotations

import numpy as np
from galpy.actionAngle import actionAngleStaeckel
from galpy.orbit import Orbit
from galpy.potential import vcirc
from numpy.typing import NDArray
from symmetries._types import GalpyPotential, PhasePoint


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
    potential: list[GalpyPotential],
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
    potential : list[GalpyPotential]
        Galpy potential list.
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

        # Correctly extract Cartesian positions across all times
        pos_out[i, :, 0] = orb.x(times)
        pos_out[i, :, 1] = orb.y(times)
        pos_out[i, :, 2] = orb.z(times)

        # Correctly extract Cartesian velocities across all times
        vel_out[i, :, 0] = orb.vx(times)
        vel_out[i, :, 1] = orb.vy(times)
        vel_out[i, :, 2] = orb.vz(times)

    return PhasePoint(pos=pos_out, vel=vel_out, time=times)


def compute_actions(
    phase: PhasePoint,
    potential: list[GalpyPotential],
    delta: float | NDArray[np.floating] = 0.5,
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """Compute the actions (J_R, L_z, J_z) using the Staeckel Fudge.

    Parameters
    ----------
    phase : PhasePoint
        Phase-space data with shape ``(n_particles, n_times, 3)``.
    potential : list[GalpyPotential]
        Galpy potential list.
    delta : float | NDArray
        Focal distance for the Staeckel approximation.  A scalar uses the
        same value everywhere; an array of shape ``(n_particles, n_times)``
        uses a per-point focal distance derived from the local radius.

    Returns
    -------
    tuple
        ``(jr, lz, jz)`` action values, each with shape ``(n_particles, n_times)``.
    """
    import time as _time

    n_particles, n_times, _ = phase.pos.shape
    jr_out = np.zeros((n_particles, n_times))
    lz_out = np.zeros((n_particles, n_times))
    jz_out = np.zeros((n_particles, n_times))

    scalar_delta = np.ndim(delta) == 0
    scalar_aa = actionAngleStaeckel(pot=potential, delta=float(delta)) if scalar_delta else None

    for i in range(n_particles):
        t0 = _time.perf_counter()
        for t in range(n_times):
            if scalar_aa is not None:
                aa = scalar_aa
            else:
                aa = actionAngleStaeckel(pot=potential, delta=float(delta[i, t]))  # type: ignore[index]
            pos_t = phase.pos[i, t]
            vel_t = phase.vel[i, t]
            r_cyl, v_r, v_t, z_val, vz_val, phi = cartesian_to_cylindrical(pos_t, vel_t)
            orb = Orbit(vxvv=[float(r_cyl), float(v_r), float(v_t), float(z_val), float(vz_val), float(phi)])
            jr_val, lz_val, jz_val = aa(orb)
            jr_out[i, t] = np.asarray(jr_val).flat[0]
            lz_out[i, t] = np.asarray(lz_val).flat[0]
            jz_out[i, t] = np.asarray(jz_val).flat[0]
        elapsed = _time.perf_counter() - t0
        print(f"  Actions particle {i + 1}/{n_particles}: {n_times} snapshots in {elapsed:.2f}s")

    return jr_out, lz_out, jz_out


class GuidingRadiusInterpolator:
    r"""Fast guiding-radius lookup via interpolation of :math:`R\,v_{\mathrm{circ}}(R)`.

    The guiding radius :math:`R_g` satisfies
    :math:`R_g \, v_{\mathrm{circ}}(R_g) = |L_z|`.  This class
    pre-evaluates the monotonic function :math:`f(R) = R\,v_c(R)` on a
    fine radial grid and uses ``np.interp`` on the inverse mapping for
    O(1) per-element lookup.  Values of :math:`|L_z|` outside the
    pre-computed range fall back to bisection.

    Parameters
    ----------
    potential : list[GalpyPotential]
        Axisymmetric galpy potential.
    r_min : float
        Inner edge of the interpolation grid.
    r_max : float
        Outer edge of the interpolation grid.
    n_grid : int
        Number of radial grid points.
    """

    def __init__(
        self,
        potential: list[GalpyPotential],
        r_min: float = 1e-4,
        r_max: float = 20.0,
        n_grid: int = 2000,
    ) -> None:
        """Initialise the interpolator by pre-computing the Lz(R) grid."""
        self._potential = potential
        self._r_min = r_min
        self._r_max = r_max

        # Build the grid: R * vcirc(R) vs R
        r_grid = np.linspace(r_min, r_max, n_grid)
        lz_grid = np.array(
            [r * float(vcirc(potential, r, use_physical=False)) for r in r_grid],
        )

        # np.interp requires the xp array to be monotonically increasing.
        # R * vcirc(R) is monotonic for physically reasonable potentials;
        # guard against numerical noise by enforcing strict increase.
        mask = np.concatenate(([True], np.diff(lz_grid) > 0))
        self._lz_grid: NDArray[np.floating] = lz_grid[mask]
        self._r_grid: NDArray[np.floating] = r_grid[mask]

        self._lz_lo = float(self._lz_grid[0])
        self._lz_hi = float(self._lz_grid[-1])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def __call__(self, lz: NDArray[np.floating]) -> NDArray[np.floating]:
        """Return guiding radii for an array of angular momenta.

        Parameters
        ----------
        lz : NDArray
            Angular momentum values (any shape).  Absolute value is used.

        Returns
        -------
        NDArray
            Guiding radii, same shape as *lz*.
        """
        abs_lz = np.abs(np.asarray(lz, dtype=np.float64))
        flat = abs_lz.ravel()

        # Interpolation for values inside the grid range
        result = np.interp(flat, self._lz_grid, self._r_grid)

        # Bisection fallback for out-of-range values
        oob = (flat < self._lz_lo) | (flat > self._lz_hi)
        if np.any(oob):
            for i in np.flatnonzero(oob):
                result[i] = self._bisect(flat[i])

        # Zero angular momentum -> zero guiding radius
        result[flat < 1e-30] = 0.0

        return result.reshape(abs_lz.shape)  # type: ignore[no-any-return]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _bisect(self, target: float, tol: float = 1e-8, max_iter: int = 80) -> float:
        lo, hi = 1e-6, self._r_max * 2.0
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            vc = float(vcirc(self._potential, mid, use_physical=False))
            if mid * vc < target:
                lo = mid
            else:
                hi = mid
            if hi - lo < tol:
                break
        return 0.5 * (lo + hi)
