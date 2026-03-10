"""Tests for the simulate command."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from click.testing import CliRunner
from experiments.commands.simulate import simulate

# Number of particles used in mock data
_N = 2

_PATCH_PREFIX = "experiments.commands.simulate"


def _make_orbit_mock() -> MagicMock:
    """Create a mock Orbit whose x/y/z/vx/vy/vz adapt to input length."""
    orb = MagicMock()
    orb.x.side_effect = lambda t: np.ones(len(t))
    orb.y.side_effect = lambda t: np.zeros(len(t))
    orb.z.side_effect = lambda t: np.zeros(len(t))
    orb.vx.side_effect = lambda t: np.zeros(len(t))
    orb.vy.side_effect = lambda t: np.ones(len(t))
    orb.vz.side_effect = lambda t: np.zeros(len(t))
    return orb


def _setup_mocks(
    mock_sample: MagicMock,
    mock_vcirc: MagicMock,
    mock_orbit_cls: MagicMock,
    mock_compute_actions: MagicMock,
    mock_compute_l_sq: MagicMock,
    mock_rg_cls: MagicMock,
    mock_build_axisym: MagicMock,
    mock_build_composite: MagicMock,
) -> None:
    """Wire up all mocks with consistent return values."""
    # sample_initial_conditions -> (r, vr, vt, z, vz, phi, labels)
    ones = np.ones(_N)
    zeros = np.zeros(_N)
    mock_sample.return_value = (ones * 0.5, zeros, ones, zeros, zeros, zeros, np.array([0, 1]))

    # vcirc -> constant 1.0
    mock_vcirc.return_value = 1.0

    # Orbit mock with dynamic-length returns
    mock_orbit_cls.return_value = _make_orbit_mock()

    # compute_actions uses side_effect to match input shape
    def _fake_actions(phase: object, _pot: object, **_kwargs: object) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        shape = getattr(phase, "pos").shape[:2]  # (n_particles, n_times)
        return np.ones(shape), np.ones(shape), np.zeros(shape)

    mock_compute_actions.side_effect = _fake_actions

    def _fake_l_sq(pos: np.ndarray, _vel: np.ndarray) -> np.ndarray:
        return np.ones(pos.shape[:2]) * 2.0

    mock_compute_l_sq.side_effect = _fake_l_sq

    # GuidingRadiusInterpolator -> callable returning constant
    rg_instance = MagicMock()
    rg_instance.side_effect = lambda lz: np.ones(len(lz)) * 0.5
    mock_rg_cls.return_value = rg_instance

    # Potentials
    mock_build_axisym.return_value = [MagicMock()]
    mock_build_composite.return_value = [MagicMock()]


class TestSimulate:
    """Tests for the simulate CLI command."""

    @patch(f"{_PATCH_PREFIX}.build_composite")
    @patch(f"{_PATCH_PREFIX}.build_axisymmetric")
    @patch(f"{_PATCH_PREFIX}.GuidingRadiusInterpolator")
    @patch(f"{_PATCH_PREFIX}.compute_l_squared")
    @patch(f"{_PATCH_PREFIX}.compute_actions")
    @patch(f"{_PATCH_PREFIX}.Orbit")
    @patch(f"{_PATCH_PREFIX}.vcirc")
    @patch(f"{_PATCH_PREFIX}.sample_initial_conditions")
    def test_creates_db_with_snapshots(
        self,
        mock_sample: MagicMock,
        mock_vcirc: MagicMock,
        mock_orbit_cls: MagicMock,
        mock_actions: MagicMock,
        mock_l_sq: MagicMock,
        mock_rg: MagicMock,
        mock_axisym: MagicMock,
        mock_composite: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Verify simulate writes snapshots to the database."""
        _setup_mocks(
            mock_sample, mock_vcirc, mock_orbit_cls, mock_actions, mock_l_sq, mock_rg, mock_axisym, mock_composite
        )

        runner = CliRunner()
        result = runner.invoke(
            simulate,
            ["--name", "test-run", "--n-particles", "4", "--outdir", str(tmp_path)],
        )

        assert result.exit_code == 0, result.output

        db_path = tmp_path / "simulations.db"
        assert db_path.exists()

        conn = sqlite3.connect(str(db_path))
        runs = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        assert runs == 1

        snaps = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
        # _N particles * default n_steps snapshots
        from experiments._models import RunConfig

        expected_steps = RunConfig(name="_test").n_steps
        assert snaps == _N * expected_steps
        conn.close()

    def test_help(self) -> None:
        """Verify --help exits cleanly and lists expected options."""
        runner = CliRunner()
        result = runner.invoke(simulate, ["--help"])
        assert result.exit_code == 0
        assert "--n-particles" in result.output
        assert "--name" in result.output

    @patch(f"{_PATCH_PREFIX}.build_composite")
    @patch(f"{_PATCH_PREFIX}.build_axisymmetric")
    @patch(f"{_PATCH_PREFIX}.GuidingRadiusInterpolator")
    @patch(f"{_PATCH_PREFIX}.compute_l_squared")
    @patch(f"{_PATCH_PREFIX}.compute_actions")
    @patch(f"{_PATCH_PREFIX}.Orbit")
    @patch(f"{_PATCH_PREFIX}.vcirc")
    @patch(f"{_PATCH_PREFIX}.sample_initial_conditions")
    def test_force_overwrites(
        self,
        mock_sample: MagicMock,
        mock_vcirc: MagicMock,
        mock_orbit_cls: MagicMock,
        mock_actions: MagicMock,
        mock_l_sq: MagicMock,
        mock_rg: MagicMock,
        mock_axisym: MagicMock,
        mock_composite: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Verify --force overwrites an existing run."""
        _setup_mocks(
            mock_sample, mock_vcirc, mock_orbit_cls, mock_actions, mock_l_sq, mock_rg, mock_axisym, mock_composite
        )

        runner = CliRunner()
        # First run
        result1 = runner.invoke(simulate, ["--name", "dup", "--n-particles", "4", "--outdir", str(tmp_path)])
        assert result1.exit_code == 0, result1.output

        # Second run without --force should fail
        result2 = runner.invoke(simulate, ["--name", "dup", "--n-particles", "4", "--outdir", str(tmp_path)])
        assert result2.exit_code != 0

        # Second run with --force should succeed
        result3 = runner.invoke(simulate, ["--name", "dup", "--n-particles", "4", "--outdir", str(tmp_path), "--force"])
        assert result3.exit_code == 0, result3.output

        conn = sqlite3.connect(str(tmp_path / "simulations.db"))
        runs = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        assert runs == 1
        conn.close()

    @patch(f"{_PATCH_PREFIX}.build_composite")
    @patch(f"{_PATCH_PREFIX}.build_axisymmetric")
    @patch(f"{_PATCH_PREFIX}.GuidingRadiusInterpolator")
    @patch(f"{_PATCH_PREFIX}.compute_l_squared")
    @patch(f"{_PATCH_PREFIX}.compute_actions")
    @patch(f"{_PATCH_PREFIX}.Orbit")
    @patch(f"{_PATCH_PREFIX}.vcirc")
    @patch(f"{_PATCH_PREFIX}.sample_initial_conditions")
    def test_seed_override(
        self,
        mock_sample: MagicMock,
        mock_vcirc: MagicMock,
        mock_orbit_cls: MagicMock,
        mock_actions: MagicMock,
        mock_l_sq: MagicMock,
        mock_rg: MagicMock,
        mock_axisym: MagicMock,
        mock_composite: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Verify --seed is forwarded to the RunConfig."""
        _setup_mocks(
            mock_sample, mock_vcirc, mock_orbit_cls, mock_actions, mock_l_sq, mock_rg, mock_axisym, mock_composite
        )

        runner = CliRunner()
        result = runner.invoke(
            simulate,
            ["--name", "seed-test", "--n-particles", "4", "--seed", "99", "--outdir", str(tmp_path)],
        )
        assert result.exit_code == 0, result.output

        conn = sqlite3.connect(str(tmp_path / "simulations.db"))
        seed_val = conn.execute("SELECT seed FROM runs WHERE name = 'seed-test'").fetchone()[0]
        assert seed_val == 99
        conn.close()

    @patch(f"{_PATCH_PREFIX}.build_composite")
    @patch(f"{_PATCH_PREFIX}.build_axisymmetric")
    @patch(f"{_PATCH_PREFIX}.GuidingRadiusInterpolator")
    @patch(f"{_PATCH_PREFIX}.compute_l_squared")
    @patch(f"{_PATCH_PREFIX}.compute_actions")
    @patch(f"{_PATCH_PREFIX}.Orbit")
    @patch(f"{_PATCH_PREFIX}.vcirc")
    @patch(f"{_PATCH_PREFIX}.sample_initial_conditions")
    def test_per_particle_dt(
        self,
        mock_sample: MagicMock,
        mock_vcirc: MagicMock,
        mock_orbit_cls: MagicMock,
        mock_actions: MagicMock,
        mock_l_sq: MagicMock,
        mock_rg: MagicMock,
        mock_axisym: MagicMock,
        mock_composite: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Verify each particle is integrated with its own fine time step."""
        _setup_mocks(
            mock_sample, mock_vcirc, mock_orbit_cls, mock_actions, mock_l_sq, mock_rg, mock_axisym, mock_composite
        )

        # Two particles with different radii -> different vcirc -> different dt
        mock_sample.return_value = (
            np.array([0.5, 2.0]),
            np.zeros(2),
            np.ones(2),
            np.zeros(2),
            np.zeros(2),
            np.zeros(2),
            np.array([0, 1]),
        )
        # Return different vcirc for each call
        mock_vcirc.side_effect = [1.0, 2.0]

        # Each orbit needs its own mock to capture separate integrate calls
        orb_mocks = [_make_orbit_mock(), _make_orbit_mock()]
        mock_orbit_cls.side_effect = orb_mocks

        runner = CliRunner()
        result = runner.invoke(
            simulate,
            ["--name", "dt-test", "--n-particles", "4", "--outdir", str(tmp_path)],
        )
        assert result.exit_code == 0, result.output

        # Orbit should have been constructed twice (once per particle)
        assert mock_orbit_cls.call_count == _N

        # Each orbit should have been integrated with different time arrays
        times_0 = orb_mocks[0].integrate.call_args[0][0]
        times_1 = orb_mocks[1].integrate.call_args[0][0]
        assert len(times_0) != len(times_1)
