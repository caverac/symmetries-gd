"""Tests for the potential-plot command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from experiments.commands.potential_plot import potential_plot


class TestPotentialPlot:
    """Tests for the potential-plot CLI command."""

    @patch("experiments.commands.potential_plot.vcirc")
    @patch("experiments.commands.potential_plot.build_axisymmetric")
    def test_generates_figure(self, mock_build: MagicMock, mock_vcirc: MagicMock, docs_img_dir: Path) -> None:
        """Verify the command creates the potential-profile PNG."""
        mock_build.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_vcirc.return_value = 1.0

        runner = CliRunner()
        result = runner.invoke(potential_plot, [])

        assert result.exit_code == 0, result.output
        assert (docs_img_dir / "potential-profile.png").exists()

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(potential_plot, ["--help"])
        assert result.exit_code == 0
