"""Tests for tensor algebra module."""

from __future__ import annotations

import numpy as np
from symmetries.tensors import (
    angular_momentum_squared,
    fradkin_tensor,
    generalized_tensor,
    lrl_tensor,
    lrl_vector,
    phi_function,
    psi_function,
    tensor_trace_squared,
)


class TestAngularMomentumSquared:
    def test_circular_orbit(self, circular_pos_vel: tuple[np.ndarray, np.ndarray]) -> None:
        pos, vel = circular_pos_vel
        result = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(result, 1.0)

    def test_radial_orbit(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([1.0, 0.0, 0.0])
        result = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(result, 0.0, atol=1e-15)

    def test_batch(self) -> None:
        pos = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        vel = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        result = angular_momentum_squared(pos, vel)
        np.testing.assert_allclose(result, [1.0, 1.0])

    def test_multidim(self) -> None:
        pos = np.zeros((3, 4, 3))
        vel = np.zeros((3, 4, 3))
        pos[..., 0] = 1.0
        vel[..., 1] = 2.0
        result = angular_momentum_squared(pos, vel)
        assert result.shape == (3, 4)
        np.testing.assert_allclose(result, 4.0)


class TestLrlVector:
    def test_circular_kepler(self) -> None:
        mu = 1.0
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        a = lrl_vector(pos, vel, mu)
        assert a.shape == (3,)
        np.testing.assert_allclose(a, [0.0, 0.0, 0.0], atol=1e-14)

    def test_batch(self) -> None:
        mu = 1.0
        pos = np.ones((2, 3, 3))
        vel = np.ones((2, 3, 3))
        result = lrl_vector(pos, vel, mu)
        assert result.shape == (2, 3, 3)


class TestLrlTensor:
    def test_shape(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = lrl_tensor(pos, vel, mu=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        rng = np.random.default_rng(0)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = lrl_tensor(pos, vel, mu=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-14)

    def test_circular_kepler_vanishes(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = lrl_tensor(pos, vel, mu=1.0)
        np.testing.assert_allclose(result, np.zeros((3, 3)), atol=1e-14)

    def test_batch(self) -> None:
        pos = np.ones((5, 3))
        vel = np.ones((5, 3))
        result = lrl_tensor(pos, vel, mu=1.0)
        assert result.shape == (5, 3, 3)


class TestFradkinTensor:
    def test_shape(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        rng = np.random.default_rng(1)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-14)

    def test_known_value(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        expected = np.zeros((3, 3))
        expected[0, 0] = 0.5  # potential: 0.5 * 1 * 1 * 1*1
        expected[1, 1] = 0.5  # kinetic: 1*1 / (2*1)
        np.testing.assert_allclose(result, expected, atol=1e-14)

    def test_batch(self) -> None:
        pos = np.ones((2, 4, 3))
        vel = np.ones((2, 4, 3))
        result = fradkin_tensor(pos, vel, omega=1.0, mass=1.0)
        assert result.shape == (2, 4, 3, 3)


class TestPsiFunction:
    def test_kepler_limit(self) -> None:
        r = np.array([0.01])
        r_core = 1.0
        mu = 1.0
        omega = 1.0
        result = psi_function(r, r_core, mu, omega)
        expected = mu / r**3
        np.testing.assert_allclose(result, expected, rtol=0.02)

    def test_harmonic_limit(self) -> None:
        r = np.array([100.0])
        r_core = 1.0
        mu = 1.0
        omega = 2.0
        result = psi_function(r, r_core, mu, omega)
        np.testing.assert_allclose(result, omega**2, rtol=1e-2)

    def test_transition(self) -> None:
        r = np.array([1.0])
        r_core = 1.0
        result = psi_function(r, r_core, mu=1.0, omega=1.0)
        assert result.shape == (1,)
        assert np.isfinite(result).all()

    def test_batch(self) -> None:
        r = np.linspace(0.1, 10.0, 50)
        result = psi_function(r, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (50,)
        assert np.all(np.isfinite(result))


class TestPhiFunction:
    def test_kepler_limit(self) -> None:
        r = np.array([0.01])
        r_core = 1.0
        mu = 1.0
        result = phi_function(r, r_core, mu)
        expected = -mu / r
        np.testing.assert_allclose(result, expected, rtol=0.02)

    def test_harmonic_limit(self) -> None:
        r = np.array([100.0])
        r_core = 1.0
        mu = 1.0
        result = phi_function(r, r_core, mu)
        np.testing.assert_allclose(result, 0.0, atol=1e-2)

    def test_batch(self) -> None:
        r = np.linspace(0.1, 10.0, 50)
        result = phi_function(r, r_core=1.0, mu=1.0)
        assert result.shape == (50,)


class TestGeneralizedTensor:
    def test_shape(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = generalized_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (3, 3)

    def test_symmetric(self) -> None:
        rng = np.random.default_rng(2)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        result = generalized_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        np.testing.assert_allclose(result, result.T, atol=1e-14)

    def test_batch(self) -> None:
        pos = np.ones((3, 4, 3))
        vel = np.ones((3, 4, 3))
        result = generalized_tensor(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (3, 4, 3, 3)

    def test_finite(self) -> None:
        rng = np.random.default_rng(3)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        result = generalized_tensor(pos, vel, r_core=0.5, mu=1.0, omega=2.0)
        assert np.all(np.isfinite(result))


class TestTensorTraceSquared:
    def test_identity(self) -> None:
        t = np.eye(3)
        result = tensor_trace_squared(t)
        np.testing.assert_allclose(result, 3.0)

    def test_zeros(self) -> None:
        t = np.zeros((3, 3))
        result = tensor_trace_squared(t)
        np.testing.assert_allclose(result, 0.0)

    def test_diagonal(self) -> None:
        t = np.diag([1.0, 2.0, 3.0])
        result = tensor_trace_squared(t)
        np.testing.assert_allclose(result, 1.0 + 4.0 + 9.0)

    def test_batch(self) -> None:
        t = np.zeros((5, 3, 3))
        for i in range(5):
            t[i] = np.eye(3) * (i + 1)
        result = tensor_trace_squared(t)
        expected = np.array([3.0 * (i + 1) ** 2 for i in range(5)])
        np.testing.assert_allclose(result, expected)

    def test_symmetric_tensor(self) -> None:
        rng = np.random.default_rng(4)
        a = rng.standard_normal((3, 3))
        t = a + a.T
        result = tensor_trace_squared(t)
        expected = np.trace(t @ t)
        np.testing.assert_allclose(result, expected)
