"""Tests for the download command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from experiments.commands.download import download


class TestDownload:
    """Tests for the download CLI command."""

    @patch("experiments.commands.download.urllib.request.urlretrieve")
    def test_downloads_file(self, mock_retrieve: MagicMock, tmp_path: Path) -> None:
        """Verify download calls urlretrieve with correct URL."""
        dest = tmp_path / "out.db"
        runner = CliRunner()
        result = runner.invoke(download, ["--environment", "staging", "--key", "test.db", "--dest", str(dest)])

        assert result.exit_code == 0, result.output
        mock_retrieve.assert_called_once_with("https://symmetries-gd-staging.s3.amazonaws.com/test.db", dest)

    @patch("experiments.commands.download.urllib.request.urlretrieve")
    def test_default_dest(self, mock_retrieve: MagicMock) -> None:
        """Verify default destination is the shared data directory."""
        runner = CliRunner()
        result = runner.invoke(download, ["--environment", "development"])

        assert result.exit_code == 0, result.output
        call_args = mock_retrieve.call_args
        assert call_args[0][1] == Path("packages/experiments/data/simulations.db")

    @patch("experiments.commands.download.urllib.request.urlretrieve")
    def test_creates_parent_directory(self, mock_retrieve: MagicMock, tmp_path: Path) -> None:
        """Verify parent directories are created if they don't exist."""
        dest = tmp_path / "nested" / "dir" / "out.db"
        runner = CliRunner()
        result = runner.invoke(download, ["--environment", "production", "--dest", str(dest)])

        assert result.exit_code == 0, result.output
        assert dest.parent.exists()
        mock_retrieve.assert_called_once()

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(download, ["--help"])
        assert result.exit_code == 0
