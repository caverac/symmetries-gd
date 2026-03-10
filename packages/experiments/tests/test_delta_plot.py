"""Tests for the delta-plot command."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner
from experiments.commands.delta_plot import delta_plot


class TestDeltaPlot:
    """Tests for the delta-plot CLI command."""

    def test_generates_figure(self, docs_img_dir: Path) -> None:
        """Verify the command creates the delta-profile PNG."""
        runner = CliRunner()
        result = runner.invoke(delta_plot, [])

        assert result.exit_code == 0, result.output
        assert (docs_img_dir / "delta-profile.png").exists()

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(delta_plot, ["--help"])
        assert result.exit_code == 0
