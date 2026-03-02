"""Tests for the simulate command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from click.testing import CliRunner
from experiments.commands.simulate import simulate
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


class TestSimulate:
    """Tests for the simulate CLI command."""

    @patch("experiments.commands.simulate.compare_variances")
    @patch("experiments.commands.simulate.compute_invariants")
    def test_creates_npz(self, mock_compute: MagicMock, mock_compare: MagicMock, tmp_path: Path) -> None:
        """Verify simulate writes a valid .npz file with expected keys."""
        mock_compute.return_value = _mock_result()
        mock_compare.return_value = _mock_comparison()

        runner = CliRunner()
        result = runner.invoke(simulate, ["-n", "2", "--n-steps", "10", "--output-dir", str(tmp_path)])

        assert result.exit_code == 0
        npz_path = tmp_path / "simulation.npz"
        assert npz_path.exists()

        data = np.load(npz_path)
        assert "c2" in data
        assert "jr" in data
        assert "var_c2" in data
        assert "median_ratio" in data
        assert "n_particles" in data
        assert int(data["n_particles"]) == 2

    @patch("experiments.commands.simulate.compare_variances")
    @patch("experiments.commands.simulate.compute_invariants")
    def test_help(self, mock_compute: MagicMock, mock_compare: MagicMock) -> None:
        """Verify --help exits cleanly and lists expected options."""
        runner = CliRunner()
        result = runner.invoke(simulate, ["--help"])
        assert result.exit_code == 0
        assert "--n-particles" in result.output
