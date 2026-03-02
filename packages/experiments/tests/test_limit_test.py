"""Tests for the limit-test command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from click.testing import CliRunner
from experiments.commands.limit_test import limit_test
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


def _mock_comparison(n: int = 2, var_c2_val: float = 1e-15) -> VarianceComparison:
    return VarianceComparison(
        var_c2=np.full(n, var_c2_val),
        var_jr=np.full(n, 1.0),
        ratio=np.full(n, var_c2_val),
        median_ratio=var_c2_val,
    )


class TestLimitTest:
    """Tests for the limit-test CLI command."""

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_creates_npz(self, mock_compute: MagicMock, mock_compare: MagicMock, tmp_path: Path) -> None:
        """Verify limit-test writes a valid NPZ with expected keys."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison()

        runner = CliRunner()
        result = runner.invoke(limit_test, ["-n", "2", "--n-steps", "10", "--output-dir", str(tmp_path)])

        assert result.exit_code == 0
        npz_path = tmp_path / "limit-test.npz"
        assert npz_path.exists()

        data = np.load(npz_path)
        for key in [
            "harmonic_var_c2",
            "harmonic_var_jr",
            "harmonic_median_var_c2",
            "kepler_var_c2",
            "kepler_var_jr",
            "kepler_median_var_c2",
            "threshold",
            "harmonic_pass",
            "kepler_pass",
            "n_particles",
        ]:
            assert key in data, f"Missing key: {key}"

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_pass_output(self, mock_compute: MagicMock, mock_compare: MagicMock, tmp_path: Path) -> None:
        """Verify PASS appears when variance is below threshold."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison(var_c2_val=1e-15)

        runner = CliRunner()
        result = runner.invoke(limit_test, ["-n", "2", "--n-steps", "10", "--output-dir", str(tmp_path)])

        assert result.exit_code == 0
        assert "PASS" in result.output

    @patch("experiments.commands._shared.compare_variances")
    @patch("experiments.commands._shared.compute_invariants")
    def test_fail_output(self, mock_compute: MagicMock, mock_compare: MagicMock, tmp_path: Path) -> None:
        """Verify FAIL appears when variance exceeds threshold."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison(var_c2_val=1.0)

        runner = CliRunner()
        result = runner.invoke(limit_test, ["-n", "2", "--n-steps", "10", "--output-dir", str(tmp_path)])

        assert result.exit_code == 0
        assert "FAIL" in result.output

    def test_help(self) -> None:
        """Verify --help lists expected options."""
        runner = CliRunner()
        result = runner.invoke(limit_test, ["--help"])
        assert result.exit_code == 0
        assert "--threshold" in result.output
