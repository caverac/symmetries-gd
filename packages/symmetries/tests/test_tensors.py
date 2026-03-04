"""Tests for tensor algebra module."""

from __future__ import annotations

import numpy as np
from symmetries.tensors import (
    angular_momentum_squared,
    fradkin_tensor,
    generalized_tensor,
    harmonic_casimir,
    kepler_casimir,
    kepler_energy,
    lrl_tensor,
    lrl_vector,
    path_tensor,
    phi_function,
    psi_function,
    sigmoid,
    tensor_trace_squared,
    traceless_fradkin,
)


class TestAngularMomentumSquared:
    """Tests for angular momentum squared computation."""

    def test_circular_orbit(self, circular_pos_vel: tuple[np.ndarray, np.ndarray]) -> None:
        """Verify unit circular orbit yields L-squared equal to one."""
        pos, vel = circular_pos_vel
        result = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(result, 1.0)

    def test_radial_orbit(self) -> None:
        """Verify radial orbit yields zero angular momentum."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([1.0, 0.0, 0.0])
        result = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(result, 0.0, atol=1e-15)

    def test_batch(self) -> None:
        """Verify batch of two orbits returns correct L-squared values."""
        pos = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        vel = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        result = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(result, [1.0, 1.0])

    def test_multidim(self) -> None:
        """Verify multi-dimensional input preserves leading shape."""
        pos = np.zeros((3, 4, 3))
        vel = np.zeros((3, 4, 3))
        pos[..., 0] = 1.0
        vel[..., 1] = 2.0
        result = angular_momentum_squared(pos, vel)
        assert result.shape == (3, 4)
        np.testing.assert_allclose(result, 4.0)


class TestLrlVector:
    """Tests for Laplace-Runge-Lenz vector."""

    def test_circular_kepler(self) -> None:
        """Verify LRL vector vanishes for circular Kepler orbit."""
        mu = 1.0
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        a = lrl_vector(pos, vel, mu)
        assert a.shape == (3,)
        np.testing.assert_allclose(a, [0.0, 0.0, 0.0], atol=1e-14)

    def test_batch(self) -> None:
        """Verify batch LRL vector returns correct shape."""
        mu = 1.0
        pos = np.ones((2, 3, 3))
        vel = np.ones((2, 3, 3))
        result = lrl_vector(pos, vel, mu)
        assert result.shape == (2, 3, 3)


class TestLrlTensor:
    """Tests for Laplace-Runge-Lenz tensor."""

    def test_shape(self) -> None:
        """Verify single phase point returns a 3x3 tensor."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = lrl_tensor(pos, vel, mu=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        """Verify LRL tensor is symmetric for random input."""
        rng = np.random.default_rng(0)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = lrl_tensor(pos, vel, mu=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-14)

    def test_circular_kepler_vanishes(self) -> None:
        """Verify LRL tensor vanishes for circular Kepler orbit."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = lrl_tensor(pos, vel, mu=1.0)
        np.testing.assert_allclose(result, np.zeros((3, 3)), atol=1e-14)

    def test_batch(self) -> None:
        """Verify batch LRL tensor returns correct shape."""
        pos = np.ones((5, 3))
        vel = np.ones((5, 3))
        result = lrl_tensor(pos, vel, mu=1.0)
        assert result.shape == (5, 3, 3)


class TestFradkinTensor:
    """Tests for the Fradkin tensor."""

    def test_shape(self) -> None:
        """Verify single phase point returns a 3x3 tensor."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        """Verify Fradkin tensor is symmetric for random input."""
        rng = np.random.default_rng(1)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-14)

    def test_known_value(self) -> None:
        """Verify Fradkin tensor matches hand-computed result for unit orbit."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        expected = np.zeros((3, 3))
        expected[0, 0] = 0.5  # potential: 0.5 * 1 * 1 * 1*1
        expected[1, 1] = 0.5  # kinetic: 1*1 / (2*1)
        np.testing.assert_allclose(result, expected, atol=1e-14)

    def test_batch(self) -> None:
        """Verify batch Fradkin tensor returns correct shape."""
        pos = np.ones((2, 4, 3))
        vel = np.ones((2, 4, 3))
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        assert result.shape == (2, 4, 3, 3)


class TestPsiFunction:
    """Tests for the psi interpolation function."""

    def test_kepler_limit(self) -> None:
        """Verify psi approaches mu/r^3 for small r."""
        r = np.array([0.01])
        r_core = 1.0
        mu = 1.0
        omega = 1.0
        result = psi_function(r, r_core, mu, omega)
        expected = mu / r**3
        np.testing.assert_allclose(result, expected, rtol=0.02)

    def test_harmonic_limit(self) -> None:
        """Verify psi approaches omega-squared for large r."""
        r = np.array([100.0])
        r_core = 1.0
        mu = 1.0
        omega = 2.0
        result = psi_function(r, r_core, mu, omega)
        np.testing.assert_allclose(result, omega**2, rtol=1e-2)

    def test_transition(self) -> None:
        """Verify psi is finite at the core radius transition."""
        r = np.array([1.0])
        r_core = 1.0
        result = psi_function(r, r_core, mu=1.0, omega=1.0)
        assert result.shape == (1,)
        assert np.isfinite(result).all()

    def test_batch(self) -> None:
        """Verify batch psi evaluation returns correct shape and finite values."""
        r = np.linspace(0.1, 10.0, 50)
        result = psi_function(r, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (50,)
        assert np.all(np.isfinite(result))


class TestPhiFunction:
    """Tests for the phi interpolation function."""

    def test_kepler_limit(self) -> None:
        """Verify phi approaches -mu/r for small r."""
        r = np.array([0.01])
        r_core = 1.0
        mu = 1.0
        result = phi_function(r, r_core, mu)
        expected = -mu / r
        np.testing.assert_allclose(result, expected, rtol=0.02)

    def test_harmonic_limit(self) -> None:
        """Verify phi approaches zero for large r."""
        r = np.array([100.0])
        r_core = 1.0
        mu = 1.0
        result = phi_function(r, r_core, mu)
        np.testing.assert_allclose(result, 0.0, atol=1e-2)

    def test_batch(self) -> None:
        """Verify batch phi evaluation returns correct shape."""
        r = np.linspace(0.1, 10.0, 50)
        result = phi_function(r, r_core=1.0, mu=1.0)
        assert result.shape == (50,)


class TestGeneralizedTensor:
    """Tests for the generalized Q_ij tensor."""

    def test_shape(self) -> None:
        """Verify single phase point returns a 3x3 tensor."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = generalized_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        """Verify generalized tensor is symmetric for random input."""
        rng = np.random.default_rng(2)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = generalized_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-14)

    def test_batch(self) -> None:
        """Verify batch generalized tensor returns correct shape."""
        pos = np.ones((3, 4, 3))
        vel = np.ones((3, 4, 3))
        result = generalized_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (3, 4, 3, 3)

    def test_finite(self) -> None:
        """Verify generalized tensor values are finite for random input."""
        rng = np.random.default_rng(3)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        result = generalized_tensor(pos, vel, r_core=0.5, mu=1.0, omega=2.0)
        assert np.all(np.isfinite(result))


class TestTensorTraceSquared:
    """Tests for Tr(T^2) computation."""

    def test_identity(self) -> None:
        """Verify Tr(I^2) equals three."""
        t = np.eye(3)
        result = tensor_trace_squared(t)
        np.testing.assert_allclose(result, 3.0)

    def test_zeros(self) -> None:
        """Verify Tr(0^2) equals zero."""
        t = np.zeros((3, 3))
        result = tensor_trace_squared(t)
        np.testing.assert_allclose(result, 0.0)

    def test_diagonal(self) -> None:
        """Verify Tr(D^2) equals sum of squared diagonal entries."""
        t = np.diag([1.0, 2.0, 3.0])
        result = tensor_trace_squared(t)
        np.testing.assert_allclose(result, 1.0 + 4.0 + 9.0)

    def test_batch(self) -> None:
        """Verify batch trace-squared returns correct per-tensor values."""
        t = np.zeros((5, 3, 3))
        for i in range(5):
            t[i] = np.eye(3) * (i + 1)
        result = tensor_trace_squared(t)
        expected = np.array([3.0 * (i + 1) ** 2 for i in range(5)])
        np.testing.assert_allclose(result, expected)

    def test_symmetric_tensor(self) -> None:
        """Verify Tr(T^2) matches numpy trace of T @ T for symmetric T."""
        rng = np.random.default_rng(4)
        a = rng.standard_normal((3, 3))
        t = a + a.T
        result = tensor_trace_squared(t)
        expected = np.trace(t @ t)
        np.testing.assert_allclose(result, expected)


class TestSigmoid:
    """Tests for the sigmoid transition function."""

    def test_small_r_approaches_zero(self) -> None:
        """Verify sigmoid approaches 0 for r << r_core."""
        r = np.array([0.01])
        result = sigmoid(r, r_core=1.0)
        assert result[0] < 0.02

    def test_large_r_approaches_one(self) -> None:
        """Verify sigmoid approaches 1 for r >> r_core."""
        r = np.array([100.0])
        result = sigmoid(r, r_core=1.0)
        assert result[0] > 0.98

    def test_midpoint(self) -> None:
        """Verify sigmoid equals 0.5 at r = r_core."""
        r = np.array([2.0])
        result = sigmoid(r, r_core=2.0)
        np.testing.assert_allclose(result, 0.5)

    def test_batch(self) -> None:
        """Verify batch sigmoid evaluation returns correct shape."""
        r = np.linspace(0.1, 10.0, 50)
        result = sigmoid(r, r_core=1.0)
        assert result.shape == (50,)
        assert np.all((result >= 0) & (result <= 1))


class TestKeplerEnergy:
    """Tests for Kepler orbital energy."""

    def test_circular_orbit(self) -> None:
        """Verify circular orbit energy E = -mu/(2r) for v = sqrt(mu/r)."""
        mu = 1.0
        r = 1.0
        pos = np.array([r, 0.0, 0.0])
        vel = np.array([0.0, np.sqrt(mu / r), 0.0])
        result = kepler_energy(pos, vel, mu)
        np.testing.assert_allclose(result, -mu / (2.0 * r))

    def test_batch(self) -> None:
        """Verify batch energy returns correct shape."""
        pos = np.ones((3, 4, 3))
        vel = np.ones((3, 4, 3))
        result = kepler_energy(pos, vel, mu=1.0)
        assert result.shape == (3, 4)


class TestKeplerCasimir:
    """Tests for the Kepler (SO(4)) Casimir."""

    def test_circular_orbit(self) -> None:
        """Verify circular orbit gives C_K = mu * r."""
        mu = 1.0
        r = 1.0
        pos = np.array([r, 0.0, 0.0])
        vel = np.array([0.0, np.sqrt(mu / r), 0.0])
        result = kepler_casimir(pos, vel, mu)
        np.testing.assert_allclose(result, mu * r, rtol=1e-8)

    def test_elliptical_orbit(self) -> None:
        """Verify C_K = mu * a for an elliptical orbit at periapsis."""
        mu = 1.0
        a = 2.0
        e = 0.5
        r_peri = a * (1.0 - e)
        v_peri = np.sqrt(mu * (2.0 / r_peri - 1.0 / a))
        pos = np.array([r_peri, 0.0, 0.0])
        vel = np.array([0.0, v_peri, 0.0])
        result = kepler_casimir(pos, vel, mu)
        np.testing.assert_allclose(result, mu * a, rtol=1e-8)

    def test_conservation_along_kepler_ellipse(self, kepler_ellipse_default: tuple[np.ndarray, np.ndarray]) -> None:
        """Verify C_K is constant at multiple points on an analytic Kepler ellipse."""
        pos, vel = kepler_ellipse_default
        mu, a = 1.0, 2.0
        c_k = kepler_casimir(pos, vel, mu)
        np.testing.assert_allclose(c_k, mu * a, rtol=1e-8)

    def test_batch(self) -> None:
        """Verify batch C_K returns correct shape."""
        pos = np.ones((5, 3))
        vel = np.ones((5, 3))
        result = kepler_casimir(pos, vel, mu=1.0)
        assert result.shape == (5,)


class TestTracelessFradkin:
    """Tests for the traceless Fradkin tensor."""

    def test_trace_is_zero(self) -> None:
        """Verify traceless Fradkin tensor has zero trace."""
        rng = np.random.default_rng(20)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        s = traceless_fradkin(pos, vel, omega=1.0, mass=1.0)
        np.testing.assert_allclose(np.trace(s), 0.0, atol=1e-14)

    def test_matches_manual(self) -> None:
        """Verify S = T - (Tr(T)/3) I matches manual computation."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        t = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        expected = t - (np.trace(t) / 3.0) * np.eye(3)
        result = traceless_fradkin(pos, vel, omega=1.0, mass=1.0)
        np.testing.assert_allclose(result, expected, atol=1e-14)

    def test_batch(self) -> None:
        """Verify batch traceless Fradkin returns correct shape."""
        pos = np.ones((2, 4, 3))
        vel = np.ones((2, 4, 3))
        result = traceless_fradkin(pos, vel, omega=1.0, mass=1.0)
        assert result.shape == (2, 4, 3, 3)


class TestHarmonicCasimir:
    """Tests for the harmonic (SU(3)) Casimir."""

    def test_circular_orbit(self) -> None:
        """Verify C_H for a unit circular harmonic orbit."""
        omega = 1.0
        mass = 1.0
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, omega, 0.0])
        result = harmonic_casimir(pos, vel, omega, mass)
        assert np.isfinite(result)
        assert result > 0

    def test_conservation_along_harmonic_orbit(self, harmonic_orbit_default: tuple[np.ndarray, np.ndarray]) -> None:
        """Verify C_H is constant along an analytic harmonic orbit."""
        pos, vel = harmonic_orbit_default
        c_h = harmonic_casimir(pos, vel, omega=1.0, mass=1.0)
        np.testing.assert_allclose(c_h, c_h[0], rtol=1e-10)

    def test_batch(self) -> None:
        """Verify batch C_H returns correct shape."""
        pos = np.ones((5, 3))
        vel = np.ones((5, 3))
        result = harmonic_casimir(pos, vel, omega=1.0, mass=1.0)
        assert result.shape == (5,)


class TestPathTensor:
    """Tests for the Lie-algebra path tensor interpolation."""

    def test_shape(self) -> None:
        """Verify single phase point returns a 3x3 tensor."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = path_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        """Verify path tensor is symmetric for random input."""
        rng = np.random.default_rng(55)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = path_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-12)

    def test_batch(self) -> None:
        """Verify batch path tensor returns correct shape."""
        pos = np.ones((3, 4, 3))
        vel = np.ones((3, 4, 3))
        result = path_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (3, 4, 3, 3)

    def test_finite(self) -> None:
        """Verify path tensor values are finite for random input."""
        rng = np.random.default_rng(66)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        result = path_tensor(pos, vel, r_core=0.5, mu=1.0, omega=2.0)
        assert np.all(np.isfinite(result))

    def test_zero_omega_uses_kepler_only(self) -> None:
        """With omega=0, harmonic term vanishes and only Kepler term remains."""
        pos = np.array([1.0, 0.5, 0.0])
        vel = np.array([0.3, 0.7, 0.1])
        result = path_tensor(pos, vel, r_core=1.0, mu=1.0, omega=0.0)
        assert result.shape == (3, 3)
        assert np.all(np.isfinite(result))
