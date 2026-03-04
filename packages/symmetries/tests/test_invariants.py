"""Tests for the deformed Casimir invariant C_2."""

from __future__ import annotations

import numpy as np
from symmetries.invariants import compute_c2
from symmetries.tensors import angular_momentum_squared


class TestComputeC2:
    """Tests for compute_c2 = L^2 + delta_eff^2 * pz^2."""

    def test_scalar_output(self) -> None:
        """Single phase point returns a scalar."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        assert result.shape == ()
        assert np.isfinite(result)

    def test_batch(self) -> None:
        """Batch of phase points returns correct shape."""
        rng = np.random.default_rng(11)
        pos = rng.standard_normal((4, 3))
        vel = rng.standard_normal((4, 3))
        result = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        assert result.shape == (4,)
        assert np.all(np.isfinite(result))

    def test_multidim(self) -> None:
        """Multi-dimensional input preserves leading dimensions."""
        rng = np.random.default_rng(12)
        pos = rng.standard_normal((2, 5, 3))
        vel = rng.standard_normal((2, 5, 3))
        result = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        assert result.shape == (2, 5)

    def test_positive_definite(self) -> None:
        """C_2 >= 0 (both terms are sums of squares)."""
        rng = np.random.default_rng(99)
        pos = rng.standard_normal((20, 3))
        vel = rng.standard_normal((20, 3))
        c2 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        assert np.all(c2 >= 0)

    def test_exceeds_l_squared(self) -> None:
        """C_2 >= L^2 because the delta_eff^2 * pz^2 term is non-negative."""
        rng = np.random.default_rng(42)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        c2 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        l_sq = angular_momentum_squared(pos, vel)
        assert np.all(c2 >= l_sq - 1e-12)

    def test_equals_l_squared_when_pz_zero(self) -> None:
        """With vz=0, pz=0 so C_2 = L^2 exactly."""
        pos = np.array([1.0, 0.5, 0.3])
        vel = np.array([0.3, 0.7, 0.0])
        c2 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        l_sq = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(c2, l_sq, rtol=1e-12)

    def test_delta_eff_grows_with_radius(self) -> None:
        """Particles further out have larger delta_eff, hence larger C_2 for same pz."""
        vel = np.array([0.0, 1.0, 1.0])
        pos_inner = np.array([0.01, 0.0, 0.0])
        pos_outer = np.array([5.0, 0.0, 0.0])
        c2_inner = compute_c2(pos_inner, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        c2_outer = compute_c2(pos_outer, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        assert c2_outer > c2_inner

    def test_parameters_affect_result(self) -> None:
        """mu, plummer_mass, plummer_scale change the output when pz != 0."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.5])
        c2_a = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        c2_b = compute_c2(pos, vel, mu=5.0, plummer_mass=2.0, plummer_scale=3.0)
        assert c2_a != c2_b

    def test_mass_affects_result(self) -> None:
        """Mass enters kinetic term pz = m * vz."""
        pos = np.array([1.0, 0.5, 0.0])
        vel = np.array([0.0, 1.0, 0.5])
        c2_m1 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5, mass=1.0)
        c2_m2 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5, mass=2.0)
        assert c2_m1 != c2_m2

    def test_disk_parameters_affect_result(self) -> None:
        """disk_mass and disk_a change delta_eff at large radii."""
        pos = np.array([5.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 1.0])
        c2_no_disk = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        c2_with_disk = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5, disk_mass=0.5, disk_a=3.0)
        assert c2_no_disk != c2_with_disk

    def test_conserved_along_harmonic_orbit(
        self,
        harmonic_orbit_default: tuple[np.ndarray, np.ndarray],
    ) -> None:
        """C_2 is approximately constant along a planar harmonic orbit (pz=0)."""
        pos, vel = harmonic_orbit_default
        plummer_mass = 1.0
        plummer_scale = 1.0
        mu = 1e-12
        c2 = compute_c2(pos, vel, mu=mu, plummer_mass=plummer_mass, plummer_scale=plummer_scale)
        # For a planar orbit (z=0, vz=0), C2 = L^2 which is conserved
        np.testing.assert_allclose(c2, c2[0], rtol=1e-6)
