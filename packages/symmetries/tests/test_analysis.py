"""Tests for the analysis pipeline and variance comparison."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
from symmetries._types import InvariantResult, PhasePoint, PotentialConfig
from symmetries.analysis import compare_variances, compute_invariants


class TestComputeInvariants:
    """Tests for the compute_invariants pipeline orchestrator."""

    @patch("symmetries.analysis.compute_actions")
    @patch("symmetries.analysis.compute_l_squared")
    @patch("symmetries.analysis.integrate_orbits")
    @patch("symmetries.analysis.build_axisymmetric")
    @patch("symmetries.analysis.build_composite")
    def test_orchestrates_pipeline(
        self,
        mock_build: MagicMock,
        mock_build_axi: MagicMock,
        mock_integrate: MagicMock,
        mock_l_sq: MagicMock,
        mock_actions: MagicMock,
    ) -> None:
        """Verify pipeline calls build, integrate, l_sq, and actions in order."""
        config = PotentialConfig()
        times = np.linspace(0, 1, 5)

        mock_build.return_value = ["pot"]
        mock_build_axi.return_value = ["axi_pot"]
        mock_phase = PhasePoint(
            pos=np.ones((2, 5, 3)),
            vel=np.ones((2, 5, 3)),
            time=times,
        )
        mock_integrate.return_value = mock_phase
        mock_l_sq.return_value = np.ones((2, 5))
        mock_actions.return_value = (np.ones((2, 5)) * 0.5, np.ones((2, 5)) * 0.1, np.ones((2, 5)) * 0.05)

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
        mock_build_axi.assert_called_once_with(config)
        mock_integrate.assert_called_once()
        mock_l_sq.assert_called_once()
        mock_actions.assert_called_once()

    @patch("symmetries.analysis.compute_actions")
    @patch("symmetries.analysis.compute_l_squared")
    @patch("symmetries.analysis.integrate_orbits")
    @patch("symmetries.analysis.build_axisymmetric")
    @patch("symmetries.analysis.build_composite")
    def test_result_fields(
        self,
        mock_build: MagicMock,
        mock_build_axi: MagicMock,
        mock_integrate: MagicMock,
        mock_l_sq: MagicMock,
        mock_actions: MagicMock,
    ) -> None:
        """Verify the InvariantResult has correct fields."""
        config = PotentialConfig()
        times = np.linspace(0, 1, 3)

        mock_build.return_value = ["pot"]
        mock_build_axi.return_value = ["axi_pot"]
        mock_integrate.return_value = PhasePoint(
            pos=np.ones((1, 3, 3)),
            vel=np.ones((1, 3, 3)),
            time=times,
        )
        mock_l_sq.return_value = np.ones((1, 3)) * 2.0
        mock_actions.return_value = (np.ones((1, 3)) * 0.5, np.ones((1, 3)) * 0.1, np.ones((1, 3)) * 0.05)

        result = compute_invariants(
            config,
            r_cyl=np.array([1.0]),
            vr=np.zeros(1),
            vt=np.ones(1),
            z=np.zeros(1),
            vz=np.zeros(1),
            phi=np.zeros(1),
            times=times,
        )

        assert result.jr.shape == (1, 3)
        assert result.jz.shape == (1, 3)
        assert result.l_sq.shape == (1, 3)
        np.testing.assert_allclose(result.jz[0, 0], 0.05)
        np.testing.assert_allclose(result.l_sq[0, 0], 2.0)


class TestCompareVariances:
    """Tests for the variance comparison utility."""

    def test_constant_jz_varying_jr(self) -> None:
        """Verify constant Jz yields zero variance and small ratio."""
        jz = np.ones((3, 10))
        jr = np.tile(np.linspace(0, 1, 10), (3, 1))
        l_sq = np.ones((3, 10))
        time = np.linspace(0, 1, 10)
        phase = PhasePoint(pos=np.zeros((3, 10, 3)), vel=np.zeros((3, 10, 3)), time=time)
        result = InvariantResult(jz=jz, jr=jr, l_sq=l_sq, time=time, phase=phase)

        vc = compare_variances(result)
        np.testing.assert_allclose(vc.var_jz, 0.0, atol=1e-15)
        assert np.all(vc.var_jr > 0)
        assert np.all(vc.ratio < 1e-10)
        assert vc.median_ratio < 1e-10

    def test_equal_variance(self) -> None:
        """Verify identical Jz and Jr data produce ratio of one."""
        rng = np.random.default_rng(30)
        data = rng.standard_normal((5, 20))
        l_sq = np.ones((5, 20))
        time = np.linspace(0, 1, 20)
        phase = PhasePoint(pos=np.zeros((5, 20, 3)), vel=np.zeros((5, 20, 3)), time=time)
        result = InvariantResult(jz=data, jr=data, l_sq=l_sq, time=time, phase=phase)

        vc = compare_variances(result)
        np.testing.assert_allclose(vc.ratio, 1.0)
        np.testing.assert_allclose(vc.median_ratio, 1.0)

    def test_shapes(self) -> None:
        """Verify output arrays have correct per-orbit shapes."""
        jz = np.ones((4, 8))
        jr = np.ones((4, 8))
        l_sq = np.ones((4, 8))
        time = np.linspace(0, 1, 8)
        phase = PhasePoint(pos=np.zeros((4, 8, 3)), vel=np.zeros((4, 8, 3)), time=time)
        result = InvariantResult(jz=jz, jr=jr, l_sq=l_sq, time=time, phase=phase)

        vc = compare_variances(result)
        assert vc.var_jz.shape == (4,)
        assert vc.var_jr.shape == (4,)
        assert vc.var_l_sq.shape == (4,)
        assert vc.ratio.shape == (4,)
