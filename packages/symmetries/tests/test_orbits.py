"""Tests for orbit integration and action computation."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from symmetries._types import PhasePoint
from symmetries.orbits import GuidingRadiusInterpolator, cartesian_to_cylindrical, compute_actions, integrate_orbits


class TestCartesianToCylindrical:
    """Tests for Cartesian to cylindrical coordinate conversion."""

    def test_on_x_axis(self) -> None:
        """Verify conversion for a point on the x-axis."""
        pos = np.array([2.0, 0.0, 1.0])
        vel = np.array([1.0, 3.0, 0.5])
        r, vr, vt, z, vz, phi = cartesian_to_cylindrical(pos, vel)
        np.testing.assert_allclose(r, 2.0)
        np.testing.assert_allclose(phi, 0.0, atol=1e-15)
        np.testing.assert_allclose(z, 1.0)
        np.testing.assert_allclose(vr, 1.0)
        np.testing.assert_allclose(vt, 3.0)
        np.testing.assert_allclose(vz, 0.5)

    def test_on_y_axis(self) -> None:
        """Verify conversion for a point on the y-axis."""
        pos = np.array([0.0, 3.0, 0.0])
        vel = np.array([-1.0, 2.0, 0.0])
        r, vr, vt, _z, _vz, phi = cartesian_to_cylindrical(pos, vel)
        np.testing.assert_allclose(r, 3.0)
        np.testing.assert_allclose(phi, np.pi / 2)
        np.testing.assert_allclose(vr, 2.0, atol=1e-14)
        np.testing.assert_allclose(vt, 1.0, atol=1e-14)

    def test_batch(self) -> None:
        """Verify batch conversion returns correct shape and radii."""
        pos = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        vel = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])
        r, _vr, _vt, _z, _vz, _phi = cartesian_to_cylindrical(pos, vel)
        assert r.shape == (2,)
        np.testing.assert_allclose(r, [1.0, 1.0])

    def test_roundtrip_radius(self) -> None:
        """Verify cylindrical radius matches Cartesian xy-magnitude."""
        rng = np.random.default_rng(20)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        r, _, _, z, _, _ = cartesian_to_cylindrical(pos, vel)
        expected_r = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2)
        np.testing.assert_allclose(r, expected_r)
        np.testing.assert_allclose(z, pos[:, 2])


class TestIntegrateOrbits:
    """Tests for galpy orbit integration wrapper."""

    @patch("symmetries.orbits.Orbit")
    def test_returns_phase_point(self, mock_orbit_cls: MagicMock) -> None:
        """Verify single orbit integration returns a PhasePoint with correct shape."""
        mock_orb = MagicMock()
        mock_orbit_cls.return_value = mock_orb

        times = np.linspace(0, 1, 5)
        mock_orb.x.return_value = np.ones(5)
        mock_orb.y.return_value = np.zeros(5)
        mock_orb.z.return_value = np.zeros(5)
        mock_orb.vx.return_value = np.zeros(5)
        mock_orb.vy.return_value = np.ones(5)
        mock_orb.vz.return_value = np.zeros(5)

        result = integrate_orbits(
            r_cyl=np.array([1.0]),
            vr=np.array([0.0]),
            vt=np.array([1.0]),
            z=np.array([0.0]),
            vz=np.array([0.0]),
            phi=np.array([0.0]),
            potential=[],
            times=times,
        )

        assert isinstance(result, PhasePoint)
        assert result.pos.shape == (1, 5, 3)
        assert result.vel.shape == (1, 5, 3)
        mock_orb.integrate.assert_called_once()

    @patch("symmetries.orbits.Orbit")
    def test_multiple_particles(self, mock_orbit_cls: MagicMock) -> None:
        """Verify multiple particles produce correctly stacked output."""
        mock_orb = MagicMock()
        mock_orbit_cls.return_value = mock_orb

        times = np.linspace(0, 1, 3)
        mock_orb.x.return_value = np.ones(3)
        mock_orb.y.return_value = np.zeros(3)
        mock_orb.z.return_value = np.zeros(3)
        mock_orb.vx.return_value = np.zeros(3)
        mock_orb.vy.return_value = np.ones(3)
        mock_orb.vz.return_value = np.zeros(3)

        result = integrate_orbits(
            r_cyl=np.array([1.0, 2.0]),
            vr=np.array([0.0, 0.0]),
            vt=np.array([1.0, 1.0]),
            z=np.array([0.0, 0.0]),
            vz=np.array([0.0, 0.0]),
            phi=np.array([0.0, 0.0]),
            potential=[],
            times=times,
        )

        assert result.pos.shape == (2, 3, 3)
        assert mock_orbit_cls.call_count == 2


class TestComputeActions:
    """Tests for Staeckel action computation."""

    @patch("symmetries.orbits.Orbit")
    @patch("symmetries.orbits.actionAngleStaeckel")
    def test_returns_jr_array(self, mock_aa_cls: MagicMock, _mock_orbit_cls: MagicMock) -> None:
        """Verify Jr array has correct shape and values."""
        mock_aa = MagicMock()
        mock_aa_cls.return_value = mock_aa
        mock_aa.return_value = (np.array([0.5]), np.array([1.0]), np.array([0.1]))

        pos = np.array([[[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]])
        vel = np.array([[[0.0, 1.0, 0.0], [0.0, 1.0, 0.0]]])
        time = np.array([0.0, 1.0])
        phase = PhasePoint(pos=pos, vel=vel, time=time)

        jr, lz, jz = compute_actions(phase, potential=[], delta=0.5)
        assert jr.shape == (1, 2)
        np.testing.assert_allclose(jr[0, 0], 0.5)
        np.testing.assert_allclose(lz[0, 0], 1.0)
        np.testing.assert_allclose(jz[0, 0], 0.1)

    @patch("symmetries.orbits.Orbit")
    @patch("symmetries.orbits.actionAngleStaeckel")
    def test_action_finder_initialised(self, mock_aa_cls: MagicMock, _mock_orbit_cls: MagicMock) -> None:
        """Verify actionAngleStaeckel is initialised with potential and delta."""
        mock_aa = MagicMock()
        mock_aa_cls.return_value = mock_aa
        mock_aa.return_value = (np.array([0.1]), np.array([0.2]), np.array([0.3]))

        pos = np.array([[[1.0, 0.0, 0.0]]])
        vel = np.array([[[0.0, 1.0, 0.0]]])
        phase = PhasePoint(pos=pos, vel=vel, time=np.array([0.0]))

        compute_actions(phase, potential=[], delta=0.7)
        mock_aa_cls.assert_called_once_with(pot=[], delta=0.7)

    @patch("symmetries.orbits.Orbit")
    @patch("symmetries.orbits.actionAngleStaeckel")
    def test_variable_delta_array(self, mock_aa_cls: MagicMock, _mock_orbit_cls: MagicMock) -> None:
        """Verify per-point delta creates a new actionAngleStaeckel per snapshot."""
        mock_aa = MagicMock()
        mock_aa_cls.return_value = mock_aa
        mock_aa.return_value = (np.array([0.5]), np.array([1.0]), np.array([0.1]))

        pos = np.array([[[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]])
        vel = np.array([[[0.0, 1.0, 0.0], [0.0, 1.0, 0.0]]])
        time = np.array([0.0, 1.0])
        phase = PhasePoint(pos=pos, vel=vel, time=time)

        delta_arr = np.array([[0.3, 0.6]])
        jr, _lz, _jz = compute_actions(phase, potential=[], delta=delta_arr)
        assert jr.shape == (1, 2)
        # Should create an actionAngleStaeckel for each (particle, time) pair
        assert mock_aa_cls.call_count == 2
        mock_aa_cls.assert_any_call(pot=[], delta=0.3)
        mock_aa_cls.assert_any_call(pot=[], delta=0.6)


class TestGuidingRadiusInterpolator:
    """Tests for the guiding-radius interpolation class."""

    @pytest.fixture()
    def interpolator(self) -> GuidingRadiusInterpolator:
        """Build an interpolator from MWPotential2014."""
        from galpy.potential import MWPotential2014

        return GuidingRadiusInterpolator(MWPotential2014)

    def test_zero_lz_returns_zero(self, interpolator: GuidingRadiusInterpolator) -> None:
        """Zero angular momentum gives zero guiding radius."""
        result = interpolator(np.array([0.0, 0.0]))
        np.testing.assert_allclose(result, 0.0)

    def test_positive_output(self, interpolator: GuidingRadiusInterpolator) -> None:
        """Positive Lz gives positive guiding radius."""
        result = interpolator(np.array([0.5, 1.0, 2.0]))
        assert np.all(result > 0)

    def test_monotonic(self, interpolator: GuidingRadiusInterpolator) -> None:
        """Larger |Lz| gives larger guiding radius."""
        lz = np.array([0.5, 1.0, 2.0, 3.0])
        rg = interpolator(lz)
        assert np.all(np.diff(rg) > 0)

    def test_negative_lz_uses_absolute(self, interpolator: GuidingRadiusInterpolator) -> None:
        """Negative Lz is treated the same as positive."""
        rg_pos = interpolator(np.array([1.0]))
        rg_neg = interpolator(np.array([-1.0]))
        np.testing.assert_allclose(rg_pos, rg_neg)

    def test_shape_preserved(self, interpolator: GuidingRadiusInterpolator) -> None:
        """Output shape matches input shape."""
        lz = np.ones((3, 4))
        result = interpolator(lz)
        assert result.shape == (3, 4)

    def test_bisection_fallback_for_large_lz(self) -> None:
        """Values outside the grid range fall back to bisection."""
        from galpy.potential import MWPotential2014

        interp = GuidingRadiusInterpolator(MWPotential2014, r_max=5.0, n_grid=100)
        # A very large Lz that is likely beyond r_max=5
        large_lz = np.array([50.0])
        result = interp(large_lz)
        assert result[0] > 0
        assert np.isfinite(result[0])


@pytest.mark.slow()
class TestIntegrationSlow:
    """Slow integration tests using real galpy potentials."""

    def test_circular_orbit_real_galpy(self) -> None:
        """Verify circular orbit integration with MWPotential2014 produces finite output."""
        from galpy.potential import MWPotential2014

        times = np.linspace(0.0, 1.0, 20)
        result = integrate_orbits(
            r_cyl=np.array([1.0]),
            vr=np.array([0.0]),
            vt=np.array([1.0]),
            z=np.array([0.0]),
            vz=np.array([0.0]),
            phi=np.array([0.0]),
            potential=MWPotential2014,
            times=times,
        )
        assert result.pos.shape == (1, 20, 3)
        assert np.all(np.isfinite(result.pos))
        assert np.all(np.isfinite(result.vel))
