"""Tests for the CLI entry point."""

from __future__ import annotations

from click.testing import CliRunner
from experiments.cli import main


class TestCLI:
    """Tests for the CLI entry point."""

    def test_help(self) -> None:
        """Verify --help exits cleanly and shows the group description."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Research CLI" in result.output

    def test_commands_listed(self) -> None:
        """Verify that all subcommands appear in --help output."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert "simulate" in result.output
        assert "limit-test" in result.output
        assert "action-scatter" in result.output
        assert "delta-plot" in result.output
        assert "migration-plot" in result.output
