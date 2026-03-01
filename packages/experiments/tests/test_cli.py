"""Tests for the CLI entry point."""

from __future__ import annotations

from click.testing import CliRunner
from experiments.cli import main


class TestCLI:
    def test_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Research CLI" in result.output

    def test_commands_listed(self) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert "simulate" in result.output
        assert "variance-plot" in result.output
