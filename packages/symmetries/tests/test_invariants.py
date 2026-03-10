"""Tests for the Staeckel focal distance and angular momentum computation."""

from __future__ import annotations

import numpy as np
from symmetries.invariants import compute_l_squared, delta_miyamoto_nagai


class TestDeltaMiyamotoNagai:
    """Tests for delta_miyamoto_nagai."""

    def test_scalar_radius(self) -> None:
        """Single radius returns a scalar."""
        result = delta_miyamoto_nagai(np.array(1.0), a=3.0, b=0.3)
        assert result.shape == ()
        assert np.isfinite(result)

    def test_batch(self) -> None:
        """Batch of radii returns correct shape."""
        radii = np.linspace(0.1, 5.0, 20)
        result = delta_miyamoto_nagai(radii, a=3.0, b=0.3)
        assert result.shape == (20,)
        assert np.all(np.isfinite(result))

    def test_non_negative(self) -> None:
        """Delta is always non-negative (clipped)."""
        radii = np.linspace(0.0, 100.0, 500)
        result = delta_miyamoto_nagai(radii, a=3.0, b=0.3)
        assert np.all(result >= 0.0)

    def test_zero_at_origin(self) -> None:
        """At R=0, Delta = sqrt(4*a*(a+b)^2 / (3*(a+b)) - 0) = sqrt(4*a*(a+b)/3)."""
        result = delta_miyamoto_nagai(np.array(0.0), a=3.0, b=0.3)
        expected = np.sqrt(4.0 * 3.0 * (3.0 + 0.3) / 3.0)
        np.testing.assert_allclose(result, expected, rtol=1e-12)

    def test_depends_on_a(self) -> None:
        """Changing scale length changes the result."""
        r = np.array(1.0)
        d1 = delta_miyamoto_nagai(r, a=3.0, b=0.3)
        d2 = delta_miyamoto_nagai(r, a=5.0, b=0.3)
        assert d1 != d2

    def test_depends_on_b(self) -> None:
        """Changing scale height changes the result."""
        r = np.array(1.0)
        d1 = delta_miyamoto_nagai(r, a=3.0, b=0.3)
        d2 = delta_miyamoto_nagai(r, a=3.0, b=1.0)
        assert d1 != d2

    def test_multidim(self) -> None:
        """Multi-dimensional input preserves leading dimensions."""
        radii = np.ones((2, 5))
        result = delta_miyamoto_nagai(radii, a=3.0, b=0.3)
        assert result.shape == (2, 5)

    def test_formula_correctness(self) -> None:
        """Verify the formula against manual calculation."""
        r = np.array(2.0)
        a, b = 3.0, 0.3
        ab = a + b
        expected_sq = 4.0 * a * (r**2 + ab**2) / (3.0 * ab) - r**2
        expected = np.sqrt(max(expected_sq, 0.0))
        result = delta_miyamoto_nagai(r, a=a, b=b)
        np.testing.assert_allclose(result, expected, rtol=1e-12)


class TestComputeLSquared:
    """Tests for compute_l_squared."""

    def test_scalar(self) -> None:
        """Single phase point returns a scalar."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([0.0, 1.0, 0.0])
        result = compute_l_squared(pos, vel)
        assert result.shape == ()
        np.testing.assert_allclose(result, 1.0, rtol=1e-12)

    def test_batch(self) -> None:
        """Batch of points returns correct shape."""
        rng = np.random.default_rng(11)
        pos = rng.standard_normal((4, 3))
        vel = rng.standard_normal((4, 3))
        result = compute_l_squared(pos, vel)
        assert result.shape == (4,)
        assert np.all(np.isfinite(result))

    def test_positive_definite(self) -> None:
        """L^2 >= 0."""
        rng = np.random.default_rng(99)
        pos = rng.standard_normal((20, 3))
        vel = rng.standard_normal((20, 3))
        result = compute_l_squared(pos, vel)
        assert np.all(result >= 0)

    def test_zero_for_parallel(self) -> None:
        """L^2 = 0 when r and v are parallel."""
        pos = np.array([1.0, 0.0, 0.0])
        vel = np.array([2.0, 0.0, 0.0])
        result = compute_l_squared(pos, vel)
        np.testing.assert_allclose(result, 0.0, atol=1e-12)

    def test_multidim(self) -> None:
        """Multi-dimensional input preserves leading dimensions."""
        rng = np.random.default_rng(12)
        pos = rng.standard_normal((2, 5, 3))
        vel = rng.standard_normal((2, 5, 3))
        result = compute_l_squared(pos, vel)
        assert result.shape == (2, 5)
