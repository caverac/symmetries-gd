"""Tests for the shared simulation helper."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
from experiments.commands._shared import run_single_simulation
from symmetries._types import InvariantResult, PhasePoint, PotentialConfig, VarianceComparison


def _mock_result(n: int = 2, nt: int = 10) -> InvariantResult:
    return InvariantResult(
        jz=np.ones((n, nt)),
        jr=np.ones((n, nt)),
        l_sq=np.ones((n, nt)),
        time=np.linspace(0, 1, nt),
        phase=PhasePoint(
            pos=np.zeros((n, nt, 3)),
            vel=np.zeros((n, nt, 3)),
            time=np.linspace(0, 1, nt),
        ),
    )


def _mock_comparison(n: int = 2) -> VarianceComparison:
    return VarianceComparison(
        var_jz=np.full(n, 0.01),
        var_jr=np.full(n, 1.0),
        var_l_sq=np.full(n, 0.05),
        ratio=np.full(n, 0.01),
        median_ratio=0.01,
    )


class TestRunSingleSimulation:
    """Tests for run_single_simulation."""

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_returns_result_and_comparison(self, mock_compute: MagicMock, mock_compare: MagicMock) -> None:
        """Verify the function returns (InvariantResult, VarianceComparison)."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison()

        config = PotentialConfig()
        result, comparison = run_single_simulation(
            config, n_particles=2, r_min=0.3, r_max=1.5, t_end=1.0, n_steps=10, seed=42
        )

        assert isinstance(result, InvariantResult)
        assert isinstance(comparison, VarianceComparison)

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_passes_config_to_compute(self, mock_compute: MagicMock, mock_compare: MagicMock) -> None:
        """Verify the config is forwarded to compute_invariants."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison()

        config = PotentialConfig(bulge_mass=0.5)
        run_single_simulation(config, n_particles=2, r_min=0.3, r_max=1.5, t_end=1.0, n_steps=10, seed=42)

        call_args = mock_compute.call_args
        assert call_args[0][0] is config
