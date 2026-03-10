"""Tests for the action-scatter command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from experiments.commands.action_scatter import action_scatter

_PATCH_PREFIX = "experiments.commands.action_scatter"


def _mock_snapshot_rows() -> list[tuple[float, ...]]:
    """Build fake snapshot rows: (particle_idx, time, jr, jz, guiding_radius, lz).

    Two particles, three time steps each.
    """
    rows: list[tuple[float, ...]] = []
    for pid in (0, 1):
        for t in (0.0, 0.5, 1.0):
            jr = 0.1 + pid * 0.05 + t * 0.02
            jz = 0.02 + pid * 0.01 + t * 0.005
            rg = 1.0 + pid * 0.1 + t * 0.01
            lz = 2.0 + pid * 0.3
            rows.append((float(pid), t, jr, jz, rg, lz))
    return rows


class TestActionScatter:
    """Tests for the action-scatter CLI command."""

    @patch(f"{_PATCH_PREFIX}.sqlite3")
    def test_generates_figure(self, mock_sqlite3: MagicMock, tmp_path: Path, docs_img_dir: Path) -> None:
        """Verify the command creates the action-scatter PNG."""
        db_path = tmp_path / "simulations.db"
        db_path.touch()

        mock_conn = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = (1,)
        mock_conn.execute.return_value.fetchall.return_value = _mock_snapshot_rows()

        runner = CliRunner()
        result = runner.invoke(action_scatter, ["--name", "test-run", "--db", str(db_path)])

        assert result.exit_code == 0, result.output
        assert (docs_img_dir / "action-scatter.png").exists()

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(action_scatter, ["--help"])
        assert result.exit_code == 0

    @patch(f"{_PATCH_PREFIX}.sqlite3")
    def test_run_not_found(self, mock_sqlite3: MagicMock, tmp_path: Path) -> None:
        """Verify non-zero exit when the run name is not in the database."""
        db_path = tmp_path / "simulations.db"
        db_path.touch()

        mock_conn = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = None

        runner = CliRunner()
        result = runner.invoke(action_scatter, ["--name", "missing", "--db", str(db_path)])

        assert result.exit_code != 0
        assert "not found" in result.output
