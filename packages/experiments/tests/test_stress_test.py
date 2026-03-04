"""Tests for the stress-test command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from click.testing import CliRunner
from experiments.commands.stress_test import stress_test
from symmetries._types import InvariantResult, PhasePoint, VarianceComparison


def _mock_result(n: int = 2, nt: int = 10) -> InvariantResult:
    return InvariantResult(
        c2=np.ones((n, nt)),
        jr=np.ones((n, nt)),
        time=np.linspace(0, 1, nt),
        phase=PhasePoint(
            pos=np.zeros((n, nt, 3)),
            vel=np.zeros((n, nt, 3)),
            time=np.linspace(0, 1, nt),
        ),
    )


def _mock_comparison(n: int = 2) -> VarianceComparison:
    return VarianceComparison(
        var_c2=np.full(n, 0.01),
        var_jr=np.full(n, 1.0),
        ratio=np.full(n, 0.01),
        median_ratio=0.01,
    )


class TestStressTest:
    """Tests for the stress-test CLI command."""

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_creates_npz_and_figure(
        self, mock_compute: MagicMock, mock_compare: MagicMock, tmp_path: Path, docs_img_dir: Path
    ) -> None:
        """Verify stress-test writes NPZ and figure with correct shapes."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison()

        runner = CliRunner()
        result = runner.invoke(
            stress_test, ["-n", "2", "--n-steps", "10", "--n-points", "3", "--output-dir", str(tmp_path)]
        )

        assert result.exit_code == 0

        npz_path = tmp_path / "stress-test.npz"
        assert npz_path.exists()
        data = np.load(npz_path)
        assert data["bar_strengths"].shape == (3,)
        assert data["median_var_c2"].shape == (3,)
        assert data["median_var_jr"].shape == (3,)

        assert (docs_img_dir / "stress-test.png").exists()

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_sweep_calls_compute_n_times(
        self, mock_compute: MagicMock, mock_compare: MagicMock, tmp_path: Path, _docs_img_dir: Path
    ) -> None:
        """Verify compute_invariants is called once per sweep point."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison()

        runner = CliRunner()
        runner.invoke(stress_test, ["-n", "2", "--n-steps", "10", "--n-points", "5", "--output-dir", str(tmp_path)])

        assert mock_compute.call_count == 5

    def test_help(self) -> None:
        """Verify --help lists expected options."""
        runner = CliRunner()
        result = runner.invoke(stress_test, ["--help"])
        assert result.exit_code == 0
        assert "--bar-min" in result.output
