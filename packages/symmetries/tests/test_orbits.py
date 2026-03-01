"""Tests for orbit integration and action computation."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from symmetries._types import PhasePoint
from symmetries.orbits import cartesian_to_cylindrical, compute_actions, integrate_orbits


class TestCartesianToCylindrical:
    def test_on_x_axis(self) -> None:
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
        pos = np.array([0.0, 3.0, 0.0])
        vel = np.array([-1.0, 2.0, 0.0])
        r, vr, vt, z, vz, phi = cartesian_to_cylindrical(pos, vel)
        np.testing.assert_allclose(r, 3.0)
        np.testing.assert_allclose(phi, np.pi / 2)
        np.testing.assert_allclose(vr, 2.0, atol=1e-14)
        np.testing.assert_allclose(vt, 1.0, atol=1e-14)

    def test_batch(self) -> None:
        pos = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        vel = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])
        r, vr, vt, z, vz, phi = cartesian_to_cylindrical(pos, vel)
        assert r.shape == (2,)
        np.testing.assert_allclose(r, [1.0, 1.0])

    def test_roundtrip_radius(self) -> None:
        rng = np.random.default_rng(20)
        pos = rng.standard_normal((10, 3))
        vel = rng.standard_normal((10, 3))
        r, _, _, z, _, _ = cartesian_to_cylindrical(pos, vel)
        expected_r = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2)
        np.testing.assert_allclose(r, expected_r)
        np.testing.assert_allclose(z, pos[:, 2])


class TestIntegrateOrbits:
    @patch("symmetries.orbits.Orbit")
    def test_returns_phase_point(self, mock_orbit_cls: MagicMock) -> None:
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
    @patch("symmetries.orbits.Orbit")
    @patch("symmetries.orbits.actionAngleStaeckel")
    def test_returns_jr_array(self, mock_aa_cls: MagicMock, mock_orbit_cls: MagicMock) -> None:
        mock_aa = MagicMock()
        mock_aa_cls.return_value = mock_aa
        mock_aa.return_value = (np.array([0.5]), np.array([1.0]), np.array([0.1]))

        pos = np.array([[[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]])
        vel = np.array([[[0.0, 1.0, 0.0], [0.0, 1.0, 0.0]]])
        time = np.array([0.0, 1.0])
        phase = PhasePoint(pos=pos, vel=vel, time=time)

        result = compute_actions(phase, potential=[], delta=0.5)
        assert result.shape == (1, 2)
        np.testing.assert_allclose(result[0, 0], 0.5)

    @patch("symmetries.orbits.Orbit")
    @patch("symmetries.orbits.actionAngleStaeckel")
    def test_delta_passed(self, mock_aa_cls: MagicMock, mock_orbit_cls: MagicMock) -> None:
        mock_aa = MagicMock()
        mock_aa_cls.return_value = mock_aa
        mock_aa.return_value = (np.array([0.1]), np.array([0.2]), np.array([0.3]))

        pos = np.array([[[1.0, 0.0, 0.0]]])
        vel = np.array([[[0.0, 1.0, 0.0]]])
        phase = PhasePoint(pos=pos, vel=vel, time=np.array([0.0]))

        compute_actions(phase, potential=[], delta=0.7)
        mock_aa_cls.assert_called_once_with(pot=[], delta=0.7)


@pytest.mark.slow()
class TestIntegrationSlow:
    def test_circular_orbit_real_galpy(self) -> None:
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
