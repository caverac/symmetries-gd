"""Tests for the deformed Casimir invariant C_2."""

from __future__ import annotations

import numpy as np
from symmetries.invariants import compute_c2
from symmetries.tensors import angular_momentum_squared, generalized_tensor, tensor_trace_squared


class TestComputeC2:
    def test_scalar_output(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = compute_c2(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == ()
        assert np.isfinite(result)

    def test_equals_l2_plus_trq2(self) -> None:
        rng = np.random.default_rng(10)
        pos = rng.standard_normal(3)
        vel = rng.standard_normal(3)
        c2 = compute_c2(pos, vel, r_core=0.5, mu=2.0, omega=1.5)
        l_sq = angular_momentum_squared(pos, vel)
        q = generalized_tensor(pos, vel, r_core=0.5, mu=2.0, omega=1.5)
        tr_q_sq = tensor_trace_squared(q)
        np.testing.assert_allclose(c2, l_sq + tr_q_sq)

    def test_batch(self) -> None:
        rng = np.random.default_rng(11)
        pos = rng.standard_normal((4, 3))
        vel = rng.standard_normal((4, 3))
        result = compute_c2(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (4,)
        assert np.all(np.isfinite(result))

    def test_multidim(self) -> None:
        rng = np.random.default_rng(12)
        pos = rng.standard_normal((2, 5, 3))
        vel = rng.standard_normal((2, 5, 3))
        result = compute_c2(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert result.shape == (2, 5)

    def test_positive(self) -> None:
        rng = np.random.default_rng(13)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        result = compute_c2(pos, vel, r_core=1.0, mu=1.0, omega=1.0)
        assert np.all(result >= 0)

    def test_mass_parameter(self) -> None:
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        c2_m1 = compute_c2(pos, vel, r_core=1.0, mu=1.0, omega=1.0, mass=1.0)
        c2_m2 = compute_c2(pos, vel, r_core=1.0, mu=1.0, omega=1.0, mass=2.0)
        assert not np.isclose(c2_m1, c2_m2)
