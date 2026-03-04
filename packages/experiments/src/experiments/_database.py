"""SQLite storage for simulation runs and per-particle snapshots."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from experiments._models import RunConfig

# RunConfig fields that map to columns in the ``runs`` table (excludes ``name``).
_CONFIG_FIELDS: tuple[str, ...] = tuple(f for f in RunConfig.model_fields.keys() if f != "name")


class SimulationDB:
    """Thin wrapper around an SQLite database for simulation results.

    Parameters
    ----------
    path : Path
        Path to the ``.db`` file.  Created if it does not exist.
    """

    def __init__(self, path: Path) -> None:
        """Open (or create) the database at *path* and ensure tables exist."""
        self._conn = sqlite3.connect(str(path))
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._create_tables()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert_run(self, config: RunConfig, *, force: bool = False) -> int:
        """Insert a run record and return its ``id``.

        Parameters
        ----------
        config : RunConfig
            Full simulation configuration.
        force : bool
            If *True*, delete an existing run with the same name first.

        Returns
        -------
        int
            The auto-incremented run id.

        Raises
        ------
        click.ClickException
            If a run with the same name already exists and *force* is False.
        """
        existing = self._conn.execute("SELECT id FROM runs WHERE name = ?", (config.name,)).fetchone()
        if existing is not None:
            if not force:
                raise click.ClickException(f"Run '{config.name}' already exists. Use --force to overwrite.")
            self._conn.execute("DELETE FROM runs WHERE id = ?", (existing[0],))

        cols = ["name"] + list(_CONFIG_FIELDS)
        placeholders = ", ".join("?" for _ in cols)
        col_names = ", ".join(cols)
        values = [config.name] + [getattr(config, f) for f in _CONFIG_FIELDS]

        cur = self._conn.execute(f"INSERT INTO runs ({col_names}) VALUES ({placeholders})", values)
        self._conn.commit()
        return cur.lastrowid  # type: ignore[return-value]

    def insert_snapshots(self, run_id: int, rows: list[tuple[object, ...]]) -> None:
        """Bulk-insert snapshot rows for a run.

        Parameters
        ----------
        run_id : int
            Foreign key referencing ``runs.id``.
        rows : list[tuple]
            Each tuple contains
            ``(particle_idx, time, r, vr, vt, z, vz, phi, jr, lz, jz, c2, guiding_radius, label)``.
        """
        self._conn.executemany(
            "INSERT INTO snapshots "
            "(run_id, particle_idx, time, r, vr, vt, z, vz, phi, jr, lz, jz, c2, guiding_radius, label) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(run_id, *row) for row in rows],
        )
        self._conn.commit()

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _create_tables(self) -> None:
        """Create the ``runs`` and ``snapshots`` tables if they do not exist."""
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT UNIQUE NOT NULL,
                seed        INTEGER NOT NULL,
                t_end       REAL NOT NULL,
                n_steps     INTEGER NOT NULL,
                delta       REAL NOT NULL,
                smbh_mass   REAL NOT NULL,
                plummer_mass REAL NOT NULL,
                plummer_scale REAL NOT NULL,
                disk_amp    REAL NOT NULL,
                disk_a      REAL NOT NULL,
                disk_b      REAL NOT NULL,
                bar_strength REAL NOT NULL,
                bar_scale   REAL NOT NULL,
                bar_tform   REAL NOT NULL,
                bar_tsteady REAL NOT NULL,
                bar_pattern_speed REAL NOT NULL,
                center_n    INTEGER NOT NULL,
                center_hr   REAL NOT NULL,
                center_sr   REAL NOT NULL,
                center_sz   REAL NOT NULL,
                center_hsr  REAL NOT NULL,
                center_hsz  REAL NOT NULL,
                center_r_min REAL NOT NULL,
                center_r_max REAL NOT NULL,
                disk_n      INTEGER NOT NULL,
                disk_hr     REAL NOT NULL,
                disk_sr     REAL NOT NULL,
                disk_sz     REAL NOT NULL,
                disk_hsr    REAL NOT NULL,
                disk_hsz    REAL NOT NULL,
                disk_r_min  REAL NOT NULL,
                disk_r_max  REAL NOT NULL,
                created_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS snapshots (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id          INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
                particle_idx    INTEGER NOT NULL,
                time            REAL NOT NULL,
                r               REAL NOT NULL,
                vr              REAL NOT NULL,
                vt              REAL NOT NULL,
                z               REAL NOT NULL,
                vz              REAL NOT NULL,
                phi             REAL NOT NULL,
                jr              REAL,
                lz              REAL,
                jz              REAL,
                c2              REAL,
                guiding_radius  REAL,
                label           INTEGER NOT NULL
            );
            """)
