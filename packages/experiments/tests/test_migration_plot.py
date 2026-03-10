"""Tests for the migration-plot command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from click.testing import CliRunner
from experiments.commands.migration_plot import _pick_particles, migration_plot


class TestPickParticles:
    """Tests for _pick_particles helper."""

    def test_returns_three_indices(self) -> None:
        """Verify three distinct indices are returned."""
        rg = np.full((5, 20), 0.8)
        rg[1, -1] = 3.0  # outward
        rg[2, -1] = 0.1  # inward
        i_stay, i_out, i_in = _pick_particles(rg)
        assert i_out == 1
        assert i_in == 2
        assert i_stay not in (i_out, i_in)

    def test_non_migrator_has_low_std(self) -> None:
        """Non-migrator is selected by smallest temporal std, not endpoint diff."""
        rg = np.full((4, 20), 0.8)
        # Particle 0: returns to start but oscillates wildly (high std)
        rg[0, 5:15] = 2.0
        # Particle 1: truly constant (low std)
        # Particle 2: outward migrator
        rg[2] = np.linspace(0.8, 2.0, 20)
        # Particle 3: inward migrator
        rg[3] = np.linspace(0.8, 0.2, 20)
        i_stay, i_out, i_in = _pick_particles(rg)
        assert i_stay == 1
        assert i_out == 2
        assert i_in == 3


def _make_snapshot_rows(n_p: int = 5, n_t: int = 4) -> list[tuple[object, ...]]:
    """Build fake snapshot rows: (particle_idx, time, jr, jz, guiding_radius)."""
    rows: list[tuple[object, ...]] = []
    times = np.linspace(0.0, 300.0, n_t)
    rng = np.random.default_rng(0)
    for pid in range(n_p):
        for t in times:
            rg = 1.0 + 0.1 * pid + 0.01 * pid * float(t)
            rows.append((pid, float(t), rng.uniform(0.0, 1.0), rng.uniform(0.0, 0.01), rg))
    return rows


class TestMigrationPlot:
    """Tests for the migration-plot CLI command."""

    @patch("experiments.commands.migration_plot.sqlite3")
    def test_generates_figure(self, mock_sql: MagicMock, tmp_path: Path, docs_img_dir: Path) -> None:
        """Verify the command creates the migration-traces PNG."""
        db_path = tmp_path / "fake.db"
        db_path.touch()

        mock_conn = MagicMock()
        mock_sql.connect.return_value = mock_conn

        run_cursor = MagicMock()
        run_cursor.fetchone.return_value = (1,)

        snap_cursor = MagicMock()
        snap_cursor.fetchall.return_value = _make_snapshot_rows()

        mock_conn.execute.side_effect = [run_cursor, snap_cursor]

        runner = CliRunner()
        result = runner.invoke(migration_plot, ["--name", "test", "--db", str(db_path)])

        assert result.exit_code == 0, result.output
        assert (docs_img_dir / "migration-traces.png").exists()

    def test_help(self) -> None:
        """Verify --help exits cleanly."""
        runner = CliRunner()
        result = runner.invoke(migration_plot, ["--help"])
        assert result.exit_code == 0

    @patch("experiments.commands.migration_plot.sqlite3")
    def test_run_not_found(self, mock_sql: MagicMock, tmp_path: Path) -> None:
        """Verify error when run name is missing."""
        db_path = tmp_path / "fake.db"
        db_path.touch()

        mock_conn = MagicMock()
        mock_sql.connect.return_value = mock_conn
        run_cursor = MagicMock()
        run_cursor.fetchone.return_value = None
        mock_conn.execute.return_value = run_cursor

        runner = CliRunner()
        result = runner.invoke(migration_plot, ["--name", "missing", "--db", str(db_path)])

        assert result.exit_code != 0
        assert "not found" in result.output
