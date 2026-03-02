"""Kill-switch test: verify C_2 conservation in harmonic and Kepler limits."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
from experiments._console import console
from experiments._constants import (
    DEFAULT_DELTA,
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
@click.option("--r-min", type=float, default=DEFAULT_R_MIN, show_default=True, help="Min initial radius (kpc).")
@click.option("--r-max", type=float, default=DEFAULT_R_MAX, show_default=True, help="Max initial radius (kpc).")
@click.option("--t-end", type=float, default=DEFAULT_T_END, show_default=True, help="Integration end time (Gyr).")
@click.option("--n-steps", type=int, default=DEFAULT_N_STEPS, show_default=True, help="Number of time steps.")
@click.option("--delta", type=float, default=DEFAULT_DELTA, show_default=True, help="Staeckel delta parameter.")
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
    delta: float,
    seed: int,
    output_dir: Path,
) -> None:
    """Kill-switch test: C_2 conservation in harmonic and Kepler limits."""
    console.print("[bold]Running harmonic limit (smbh_mass~0)...[/bold]")
    harmonic_config = PotentialConfig(smbh_mass=1e-10, plummer_mass=1.0, bar_strength=0.0)
    _, harmonic_comp = run_single_simulation(harmonic_config, n_particles, r_min, r_max, t_end, n_steps, delta, seed)

    console.print("[bold]Running Kepler limit (plummer_mass~0)...[/bold]")
    kepler_config = PotentialConfig(smbh_mass=1.0, plummer_mass=0.0, bar_strength=0.0)
    _, kepler_comp = run_single_simulation(kepler_config, n_particles, r_min, r_max, t_end, n_steps, delta, seed)

    harmonic_median = float(np.median(harmonic_comp.var_c2))
    kepler_median = float(np.median(kepler_comp.var_c2))
    harmonic_pass = harmonic_median < threshold
    kepler_pass = kepler_median < threshold

    table = Table(title="Limit Test Results")
    table.add_column("Limit", style="bold")
    table.add_column("Median Var(C_2)")
    table.add_column("Threshold")
    table.add_column("Status")

    h_status = "[green]PASS[/green]" if harmonic_pass else "[red]FAIL[/red]"
    k_status = "[green]PASS[/green]" if kepler_pass else "[red]FAIL[/red]"

    table.add_row("Harmonic", f"{harmonic_median:.6e}", f"{threshold:.1e}", h_status)
    table.add_row("Kepler", f"{kepler_median:.6e}", f"{threshold:.1e}", k_status)

    console.print(table)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "limit-test.npz"

    np.savez(
        out_path,
        harmonic_var_c2=harmonic_comp.var_c2,
        harmonic_var_jr=harmonic_comp.var_jr,
        harmonic_median_var_c2=np.array(harmonic_median),
        kepler_var_c2=kepler_comp.var_c2,
        kepler_var_jr=kepler_comp.var_jr,
        kepler_median_var_c2=np.array(kepler_median),
        threshold=np.array(threshold),
        harmonic_pass=np.array(harmonic_pass),
        kepler_pass=np.array(kepler_pass),
        n_particles=np.array(n_particles),
    )

    console.print(f"Saved: {out_path}")
