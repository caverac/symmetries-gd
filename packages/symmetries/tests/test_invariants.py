"""Tests for the deformed Casimir invariant C_2."""

from __future__ import annotations

import numpy as np
from symmetries.invariants import compute_c2
from symmetries.tensors import angular_momentum_squared, harmonic_casimir


class TestComputeC2:
    """Tests for compute_c2 = L^2 + Tr(Q_tilde^2) / omega^2."""

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
        """C_2 > L^2 for generic orbits (tensor term > 0)."""
        rng = np.random.default_rng(42)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        c2 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        l_sq = angular_momentum_squared(pos, vel)
        assert np.all(c2 >= l_sq - 1e-12)
        assert np.any(c2 > l_sq + 1e-12)

    def test_matches_harmonic_casimir(self) -> None:
        """With tiny mu (sigma ~ 1), C_2 ~ C_H from harmonic_casimir()."""
        rng = np.random.default_rng(77)
        pos = rng.uniform(0.5, 2.0, (10, 3))
        vel = rng.standard_normal((10, 3))
        plummer_mass = 0.9
        plummer_scale = 0.5
        mu = 1e-12
        omega = np.sqrt(plummer_mass / plummer_scale**3)
        mass = 1.0
        c2 = compute_c2(pos, vel, mu=mu, plummer_mass=plummer_mass, plummer_scale=plummer_scale, mass=mass)
        c_h = harmonic_casimir(pos, vel, omega=omega, mass=mass)
        np.testing.assert_allclose(c2, c_h, rtol=1e-6)

    def test_conserved_along_harmonic_orbit(
        self,
        harmonic_orbit_default: tuple[np.ndarray, np.ndarray],
    ) -> None:
        """C_2 is constant along an analytic harmonic orbit when mu ~ 0."""
        pos, vel = harmonic_orbit_default
        omega = 1.0
        plummer_mass = omega**2
        plummer_scale = 1.0
        mu = 1e-12
        c2 = compute_c2(pos, vel, mu=mu, plummer_mass=plummer_mass, plummer_scale=plummer_scale)
        np.testing.assert_allclose(c2, c2[0], rtol=1e-6)

    def test_parameters_affect_result(self) -> None:
        """mu, plummer_mass, plummer_scale now change the output."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        c2_a = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5)
        c2_b = compute_c2(pos, vel, mu=5.0, plummer_mass=2.0, plummer_scale=3.0)
        assert c2_a != c2_b

    def test_mass_affects_result(self) -> None:
        """Mass enters kinetic term p_i p_j / (2m)."""
        pos = np.array([1.0, 0.5, 0.0])
        vel = np.array([0.0, 1.0, 0.5])
        c2_m1 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5, mass=1.0)
        c2_m2 = compute_c2(pos, vel, mu=0.1, plummer_mass=0.9, plummer_scale=0.5, mass=2.0)
        assert c2_m1 != c2_m2
