"""Limit test: verify J_z conservation in pure bulge and pure disk limits."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from experiments._console import console
from experiments._constants import (
    DEFAULT_LIMIT_N_PARTICLES,
    DEFAULT_LIMIT_THRESHOLD,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_T_END,
)
from experiments.commands._shared import run_single_simulation
from rich.table import Table
from symmetries import PotentialConfig


@click.command("limit-test")
@click.option("-n", "--n-particles", type=int, default=DEFAULT_LIMIT_N_PARTICLES, show_default=True, help="Particles.")
@click.option("--threshold", type=float, default=DEFAULT_LIMIT_THRESHOLD, show_default=True, help="PASS/FAIL cutoff.")
@click.option("--r-min", type=float, default=DEFAULT_R_MIN, show_default=True, help="Min initial radius.")
@click.option("--r-max", type=float, default=DEFAULT_R_MAX, show_default=True, help="Max initial radius.")
@click.option("--t-end", type=float, default=DEFAULT_T_END, show_default=True, help="Integration end time.")
@click.option("--n-steps", type=int, default=DEFAULT_N_STEPS, show_default=True, help="Number of time steps.")
@click.option("--seed", type=int, default=DEFAULT_SEED, show_default=True, help="Random seed.")
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    show_default=True,
    help="Output directory for NPZ file.",
)
def limit_test(
    n_particles: int,
    threshold: float,
    r_min: float,
    r_max: float,
    t_end: float,
    n_steps: int,
    seed: int,
    output_dir: Path,
) -> None:
    """Limit test: J_z conservation in pure bulge and pure disk limits."""
    console.print("[bold]Running spherical limit (disk_mass~0)...[/bold]")
    bulge_config = PotentialConfig(bulge_mass=1.0, disk_mass=1e-10, halo_amp=0.0, bar_strength=0.0)
    _, bulge_comp = run_single_simulation(bulge_config, n_particles, r_min, r_max, t_end, n_steps, seed)

    console.print("[bold]Running disk limit (bulge_mass~0)...[/bold]")
    disk_config = PotentialConfig(bulge_mass=1e-10, disk_mass=1.0, halo_amp=0.0, bar_strength=0.0)
    _, disk_comp = run_single_simulation(disk_config, n_particles, r_min, r_max, t_end, n_steps, seed)

    bulge_median = float(np.median(bulge_comp.var_jz))
    disk_median = float(np.median(disk_comp.var_jz))
    bulge_pass = bulge_median < threshold
    disk_pass = disk_median < threshold

    table = Table(title="Limit Test Results")
    table.add_column("Limit", style="bold")
    table.add_column("Median Var(J_z)")
    table.add_column("Threshold")
    table.add_column("Status")

    b_status = "[green]PASS[/green]" if bulge_pass else "[red]FAIL[/red]"
    d_status = "[green]PASS[/green]" if disk_pass else "[red]FAIL[/red]"

    table.add_row("Spherical (bulge)", f"{bulge_median:.6e}", f"{threshold:.1e}", b_status)
    table.add_row("Disk", f"{disk_median:.6e}", f"{threshold:.1e}", d_status)

    console.print(table)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "limit-test.npz"

    np.savez(
        out_path,
        bulge_var_jz=bulge_comp.var_jz,
        bulge_var_jr=bulge_comp.var_jr,
        bulge_median_var_jz=np.array(bulge_median),
        disk_var_jz=disk_comp.var_jz,
        disk_var_jr=disk_comp.var_jr,
        disk_median_var_jz=np.array(disk_median),
        threshold=np.array(threshold),
        bulge_pass=np.array(bulge_pass),
        disk_pass=np.array(disk_pass),
        n_particles=np.array(n_particles),
    )

    console.print(f"Saved: {out_path}")
