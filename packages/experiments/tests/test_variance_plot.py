"""Tests for the variance-plot command."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner
from experiments.commands.variance_plot import variance_plot


class TestVariancePlot:
    """Tests for the variance-plot CLI command."""

    def test_generates_figure(self, simulation_data_dir: Path, docs_img_dir: Path) -> None:
        """Verify the command creates the variance-comparison PNG."""
        runner = CliRunner()
        result = runner.invoke(variance_plot, ["--data-dir", str(simulation_data_dir)])

        assert result.exit_code == 0
        assert (docs_img_dir / "variance-comparison.png").exists()

    def test_missing_npz(self, tmp_path: Path) -> None:
        """Verify the command exits with code 1 when no .npz file exists."""
        runner = CliRunner()
        result = runner.invoke(variance_plot, ["--data-dir", str(tmp_path)])

        assert result.exit_code == 1

    def test_help(self) -> None:
        """Verify --help exits cleanly and lists --data-dir option."""
        runner = CliRunner()
        result = runner.invoke(variance_plot, ["--help"])
        assert result.exit_code == 0
        assert "--data-dir" in result.output
