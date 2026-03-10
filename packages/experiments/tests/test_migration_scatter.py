"""Tests for the migration-scatter command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from experiments.commands.migration_scatter import migration_scatter

_PATCH_PREFIX = "experiments.commands.migration_scatter"


def _mock_snapshot_rows() -> list[tuple[float, ...]]:
    """Build fake snapshot rows: (particle_idx, time, guiding_radius).

    Two particles, three time steps each.
    """
    rows: list[tuple[float, ...]] = []
    for pid in (0, 1):
        for t in (0.0, 0.5, 1.0):
            rows.append((float(pid), t, 1.0 + pid * 0.1 + t * 0.01))
    return rows


class TestMigrationScatter:
    """Tests for the migration-scatter CLI command."""

    @patch(f"{_PATCH_PREFIX}.sqlite3")
    def test_generates_figure(self, mock_sqlite3: MagicMock, tmp_path: Path, docs_img_dir: Path) -> None:
        """Verify the command creates the migration-scatter PNG."""
        db_path = tmp_path / "simulations.db"
        db_path.touch()

        mock_conn = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn

        # First execute call returns run row (id, bar_pattern_speed).
        # Second execute call returns snapshot rows.
        mock_cursor_run = MagicMock()
        mock_cursor_run.fetchone.return_value = (1, 1.45)

        mock_cursor_snaps = MagicMock()
        mock_cursor_snaps.fetchall.return_value = _mock_snapshot_rows()

        mock_conn.execute.side_effect = [mock_cursor_run, mock_cursor_snaps]

        runner = CliRunner()
        result = runner.invoke(migration_scatter, ["--name", "test-run", "--db", str(db_path)])

        assert result.exit_code == 0, result.output
        assert (docs_img_dir / "migration-scatter.png").exists()

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(migration_scatter, ["--help"])
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
        result = runner.invoke(migration_scatter, ["--name", "missing", "--db", str(db_path)])

        assert result.exit_code != 0
        assert "not found" in result.output
