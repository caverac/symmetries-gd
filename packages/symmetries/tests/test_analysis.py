"""Tests for the analysis pipeline and variance comparison."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
from symmetries._types import InvariantResult, PhasePoint, PotentialConfig
from symmetries.analysis import compare_variances, compute_invariants, omega_from_plummer, smbh_influence_radius


class TestOmegaFromPlummer:
    """Tests for Plummer angular frequency derivation."""

    def test_unit_values(self) -> None:
        """Verify unit mass and unit scale yield omega = 1."""
        result = omega_from_plummer(mass=1.0, scale=1.0)
        np.testing.assert_allclose(result, 1.0)

    def test_known_values(self) -> None:
        """Verify known mass and scale produce expected omega."""
        result = omega_from_plummer(mass=8.0, scale=2.0)
        np.testing.assert_allclose(result, 1.0)

    def test_large_mass(self) -> None:
        """Verify large mass scales correctly against analytic formula."""
        result = omega_from_plummer(mass=1e10, scale=0.5)
        expected = np.sqrt(1e10 / 0.5**3)
        np.testing.assert_allclose(result, expected)


class TestSmbhInfluenceRadius:
    """Tests for the SMBH sphere-of-influence radius."""

    def test_formula(self) -> None:
        """Verify r_infl = mu * a / M."""
        result = smbh_influence_radius(mu=0.1, bulge_mass=0.9, bulge_scale=0.5)
        np.testing.assert_allclose(result, 0.1 * 0.5 / 0.9)

    def test_scales_with_mu(self) -> None:
        """Verify doubling mu doubles the influence radius."""
        r1 = smbh_influence_radius(mu=0.1, bulge_mass=1.0, bulge_scale=1.0)
        r2 = smbh_influence_radius(mu=0.2, bulge_mass=1.0, bulge_scale=1.0)
        np.testing.assert_allclose(r2, 2.0 * r1)


class TestComputeInvariants:
    """Tests for the compute_invariants pipeline orchestrator."""

    @patch("symmetries.analysis.compute_actions")
    @patch("symmetries.analysis.compute_c2")
    @patch("symmetries.analysis.integrate_orbits")
    @patch("symmetries.analysis.build_axisymmetric")
    @patch("symmetries.analysis.build_composite")
    def test_orchestrates_pipeline(
        self,
        mock_build: MagicMock,
        mock_build_axi: MagicMock,
        mock_integrate: MagicMock,
        mock_c2: MagicMock,
        mock_actions: MagicMock,
    ) -> None:
        """Verify pipeline calls build, integrate, c2, and actions in order."""
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
        mock_build_axi.assert_called_once_with(config)
        mock_integrate.assert_called_once()
        mock_c2.assert_called_once()
        mock_actions.assert_called_once()

    @patch("symmetries.analysis.compute_actions")
    @patch("symmetries.analysis.compute_c2")
    @patch("symmetries.analysis.integrate_orbits")
    @patch("symmetries.analysis.build_axisymmetric")
    @patch("symmetries.analysis.build_composite")
    def test_passes_delta(
        self,
        mock_build: MagicMock,
        mock_build_axi: MagicMock,
        mock_integrate: MagicMock,
        mock_c2: MagicMock,
        mock_actions: MagicMock,
    ) -> None:
        """Verify delta parameter is forwarded to compute_actions."""
        config = PotentialConfig()
        times = np.linspace(0, 1, 3)

        mock_build.return_value = ["pot"]
        mock_build_axi.return_value = ["axi_pot"]
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
    """Tests for the variance comparison utility."""

    def test_constant_c2_varying_jr(self) -> None:
        """Verify constant C2 yields zero variance and small ratio."""
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
        """Verify identical C2 and Jr data produce ratio of one."""
        rng = np.random.default_rng(30)
        data = rng.standard_normal((5, 20))
        time = np.linspace(0, 1, 20)
        phase = PhasePoint(pos=np.zeros((5, 20, 3)), vel=np.zeros((5, 20, 3)), time=time)
        result = InvariantResult(c2=data, jr=data, time=time, phase=phase)

        vc = compare_variances(result)
        np.testing.assert_allclose(vc.ratio, 1.0)
        np.testing.assert_allclose(vc.median_ratio, 1.0)

    def test_shapes(self) -> None:
        """Verify output arrays have correct per-orbit shapes."""
        c2 = np.ones((4, 8))
        jr = np.ones((4, 8))
        time = np.linspace(0, 1, 8)
        phase = PhasePoint(pos=np.zeros((4, 8, 3)), vel=np.zeros((4, 8, 3)), time=time)
        result = InvariantResult(c2=c2, jr=jr, time=time, phase=phase)

        vc = compare_variances(result)
        assert vc.var_c2.shape == (4,)
        assert vc.var_jr.shape == (4,)
        assert vc.ratio.shape == (4,)
