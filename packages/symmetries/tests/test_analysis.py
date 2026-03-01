"""Tests for the analysis pipeline and variance comparison."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
from symmetries._types import InvariantResult, PhasePoint, PotentialConfig
from symmetries.analysis import compare_variances, compute_invariants, omega_from_plummer


class TestOmegaFromPlummer:
    def test_unit_values(self) -> None:
        result = omega_from_plummer(mass=1.0, scale=1.0)
        np.testing.assert_allclose(result, 1.0)

    def test_known_values(self) -> None:
        result = omega_from_plummer(mass=8.0, scale=2.0)
        np.testing.assert_allclose(result, 1.0)

    def test_large_mass(self) -> None:
        result = omega_from_plummer(mass=1e10, scale=0.5)
        expected = np.sqrt(1e10 / 0.5**3)
        np.testing.assert_allclose(result, expected)


class TestComputeInvariants:
    @patch("symmetries.analysis.compute_actions")
    @patch("symmetries.analysis.compute_c2")
    @patch("symmetries.analysis.integrate_orbits")
    @patch("symmetries.analysis.build_composite")
    def test_orchestrates_pipeline(
        self,
        mock_build: MagicMock,
        mock_integrate: MagicMock,
        mock_c2: MagicMock,
        mock_actions: MagicMock,
    ) -> None:
        config = PotentialConfig()
        times = np.linspace(0, 1, 5)

        mock_build.return_value = ["pot"]
        mock_phase = PhasePoint(
            pos=np.ones((2, 5, 3)),
            vel=np.ones((2, 5, 3)),
            time=times,
        )
        mock_integrate.return_value = mock_phase
        mock_c2.return_value = np.ones((2, 5))
        mock_actions.return_value = np.ones((2, 5)) * 0.5

        result = compute_invariants(
            config,
            r_cyl=np.array([1.0, 2.0]),
            vr=np.zeros(2),
            vt=np.ones(2),
            z=np.zeros(2),
            vz=np.zeros(2),
            phi=np.zeros(2),
            times=times,
        )

        assert isinstance(result, InvariantResult)
        mock_build.assert_called_once_with(config)
        mock_integrate.assert_called_once()
        mock_c2.assert_called_once()
        mock_actions.assert_called_once()

    @patch("symmetries.analysis.compute_actions")
    @patch("symmetries.analysis.compute_c2")
    @patch("symmetries.analysis.integrate_orbits")
    @patch("symmetries.analysis.build_composite")
    def test_passes_delta(
        self,
        mock_build: MagicMock,
        mock_integrate: MagicMock,
        mock_c2: MagicMock,
        mock_actions: MagicMock,
    ) -> None:
        config = PotentialConfig()
        times = np.linspace(0, 1, 3)

        mock_build.return_value = ["pot"]
        mock_integrate.return_value = PhasePoint(
            pos=np.ones((1, 3, 3)),
            vel=np.ones((1, 3, 3)),
            time=times,
        )
        mock_c2.return_value = np.ones((1, 3))
        mock_actions.return_value = np.ones((1, 3))

        compute_invariants(
            config,
            r_cyl=np.array([1.0]),
            vr=np.zeros(1),
            vt=np.ones(1),
            z=np.zeros(1),
            vz=np.zeros(1),
            phi=np.zeros(1),
            times=times,
            delta=0.7,
        )

        mock_actions.assert_called_once()
        _, kwargs = mock_actions.call_args
        assert kwargs["delta"] == 0.7


class TestCompareVariances:
    def test_constant_c2_varying_jr(self) -> None:
        c2 = np.ones((3, 10))
        jr = np.tile(np.linspace(0, 1, 10), (3, 1))
        time = np.linspace(0, 1, 10)
        phase = PhasePoint(pos=np.zeros((3, 10, 3)), vel=np.zeros((3, 10, 3)), time=time)
        result = InvariantResult(c2=c2, jr=jr, time=time, phase=phase)

        vc = compare_variances(result)
        np.testing.assert_allclose(vc.var_c2, 0.0, atol=1e-15)
        assert np.all(vc.var_jr > 0)
        assert np.all(vc.ratio < 1e-10)
        assert vc.median_ratio < 1e-10

    def test_equal_variance(self) -> None:
        rng = np.random.default_rng(30)
        data = rng.standard_normal((5, 20))
        time = np.linspace(0, 1, 20)
        phase = PhasePoint(pos=np.zeros((5, 20, 3)), vel=np.zeros((5, 20, 3)), time=time)
        result = InvariantResult(c2=data, jr=data, time=time, phase=phase)

        vc = compare_variances(result)
        np.testing.assert_allclose(vc.ratio, 1.0)
        np.testing.assert_allclose(vc.median_ratio, 1.0)

    def test_shapes(self) -> None:
        c2 = np.ones((4, 8))
        jr = np.ones((4, 8))
        time = np.linspace(0, 1, 8)
        phase = PhasePoint(pos=np.zeros((4, 8, 3)), vel=np.zeros((4, 8, 3)), time=time)
        result = InvariantResult(c2=c2, jr=jr, time=time, phase=phase)

        vc = compare_variances(result)
        assert vc.var_c2.shape == (4,)
        assert vc.var_jr.shape == (4,)
        assert vc.ratio.shape == (4,)
