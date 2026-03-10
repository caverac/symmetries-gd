"""Tests for the upload command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from experiments.commands.upload import upload


class TestUpload:
    """Tests for the upload CLI command."""

    @patch("experiments.commands.upload.boto3")
    def test_uploads_file(self, mock_boto3: MagicMock, tmp_path: Path) -> None:
        """Verify upload calls S3 client with correct arguments."""
        src_file = tmp_path / "simulations.db"
        src_file.write_text("test")

        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        runner = CliRunner()
        result = runner.invoke(upload, ["--environment", "staging", "--key", "test.db", "--src", str(src_file)])

        assert result.exit_code == 0, result.output
        mock_client.upload_file.assert_called_once_with(str(src_file), "symmetries-gd-staging", "test.db")

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(upload, ["--help"])
        assert result.exit_code == 0
