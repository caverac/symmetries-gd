"""Run orbit integration and store results in SQLite."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from experiments._console import console
from experiments._database import SimulationDB
from experiments._models import RunConfig
from symmetries import GuidingRadiusInterpolator, compute_invariants, sample_initial_conditions
from symmetries.orbits import cartesian_to_cylindrical
from symmetries.potentials import build_axisymmetric


@click.command()
@click.option("--name", required=True, help="Unique simulation name.")
@click.option("--seed", type=int, default=None, help="Override random seed.")
@click.option("--n-particles", type=int, default=None, help="Override total particle count (split 50/50).")
@click.option(
    "--outdir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("packages/experiments/data"),
    show_default=True,
    help="Database directory.",
)
@click.option("--force/--no-force", default=False, help="Overwrite existing run with same name.")
def simulate(
    name: str,
    seed: int | None,
    n_particles: int | None,
    outdir: Path,
    force: bool,
) -> None:
    """Run orbit integration and store results in SQLite."""
    # Build config with optional overrides
    overrides: dict[str, object] = {"name": name}
    if seed is not None:
        overrides["seed"] = seed
    if n_particles is not None:
        half = n_particles // 2
        overrides["center_n"] = half
        overrides["disk_n"] = n_particles - half

    config = RunConfig(**overrides)  # type: ignore[arg-type]

    # Database
    outdir.mkdir(parents=True, exist_ok=True)
    db = SimulationDB(outdir / "simulations.db")
    try:
        run_id = db.insert_run(config, force=force)

        # Initial conditions (always DF-based)
        pot_config = config.to_potential_config()
        ic_config = config.to_ic_config()

        console.print("[bold]Sampling DF-based initial conditions...[/bold]")
        r_cyl, vr, vt, z, vz, phi, labels = sample_initial_conditions(ic_config, pot_config)
        total = len(r_cyl)

        # Time array with dt=1
        times = np.arange(0.0, config.t_end + 1.0, 1.0)

        console.print(f"[bold]Integrating {total} orbits for {len(times)} timesteps...[/bold]")
        result = compute_invariants(pot_config, r_cyl, vr, vt, z, vz, phi, times, delta=config.delta)

        # Extract cylindrical coordinates at every timestep
        pos = result.phase.pos  # (n_particles, n_times, 3)
        vel = result.phase.vel  # (n_particles, n_times, 3)
        r_all, vr_all, vt_all, z_all, vz_all, phi_all = cartesian_to_cylindrical(pos, vel)
        # Lz = R * vT
        lz_all = r_all * vt_all

        # Guiding radii via interpolation (built once, queried per-timestep)
        console.print("[bold]Computing guiding radii...[/bold]")
        axisym = build_axisymmetric(pot_config)
        rg_interp = GuidingRadiusInterpolator(axisym)
        n_times = len(times)
        rg_all = np.zeros_like(lz_all)
        for t_idx in range(n_times):
            rg_all[:, t_idx] = rg_interp(lz_all[:, t_idx])

        # Build snapshot rows
        console.print("[bold]Writing snapshots to database...[/bold]")
        rows: list[tuple[object, ...]] = []
        for p in range(total):
            lab = int(labels[p])
            for t_idx in range(n_times):
                rows.append(
                    (
                        p,
                        float(times[t_idx]),
                        float(r_all[p, t_idx]),
                        float(vr_all[p, t_idx]),
                        float(vt_all[p, t_idx]),
                        float(z_all[p, t_idx]),
                        float(vz_all[p, t_idx]),
                        float(phi_all[p, t_idx]),
                        float(result.jr[p, t_idx]),
                        float(lz_all[p, t_idx]),
                        None,  # jz not stored
                        float(result.c2[p, t_idx]),
                        float(rg_all[p, t_idx]),
                        lab,
                    )
                )
        db.insert_snapshots(run_id, rows)

        console.print(f"[green]Done.[/green] Run '{name}' (id={run_id}): {total} particles, {n_times} timesteps.")
        console.print(f"  Total snapshots: {len(rows)}")
        console.print(f"  Database: {outdir / 'simulations.db'}")
    finally:
        db.close()
