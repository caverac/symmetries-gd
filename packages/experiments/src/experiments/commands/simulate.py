"""Run orbit integration and save results to NPZ."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
import numpy as np
from experiments._console import console
from experiments._constants import (
    DEFAULT_DELTA,
    DEFAULT_N_PARTICLES,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_T_END,
)
from symmetries import PotentialConfig, compare_variances, compute_invariants


@click.command()
@click.option("-n", "--n-particles", type=int, default=DEFAULT_N_PARTICLES, show_default=True, help="Test particles.")
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
@click.option("--smbh-mass", type=float, default=None, help="SMBH Kepler potential amplitude.")
@click.option("--plummer-mass", type=float, default=None, help="Plummer bulge amplitude.")
@click.option("--plummer-scale", type=float, default=None, help="Plummer sphere scale radius.")
@click.option("--bar-strength", type=float, default=None, help="Dehnen bar strength Af.")
@click.option("--bar-scale", type=float, default=None, help="Dehnen bar radius rb.")
@click.option("--bar-tform", type=float, default=None, help="Bar formation time.")
@click.option("--bar-tsteady", type=float, default=None, help="Bar steady-state timescale.")
@click.option("--bar-pattern-speed", type=float, default=None, help="Bar pattern speed.")
def simulate(
    n_particles: int,
    r_min: float,
    r_max: float,
    t_end: float,
    n_steps: int,
    delta: float,
    seed: int,
    output_dir: Path,
    smbh_mass: Optional[float],
    plummer_mass: Optional[float],
    plummer_scale: Optional[float],
    bar_strength: Optional[float],
    bar_scale: Optional[float],
    bar_tform: Optional[float],
    bar_tsteady: Optional[float],
    bar_pattern_speed: Optional[float],
) -> None:
    """Run orbit integration and save results to NPZ."""
    rng = np.random.default_rng(seed)

    r_cyl = rng.uniform(r_min, r_max, size=n_particles)
    vr = np.zeros(n_particles)
    vt = np.ones(n_particles)
    z = np.zeros(n_particles)
    vz = np.zeros(n_particles)
    phi = rng.uniform(0, 2 * np.pi, size=n_particles)

    times = np.linspace(0.0, t_end, n_steps)

    config_fields: dict[str, float] = {}
    for name, val in [
        ("smbh_mass", smbh_mass),
        ("plummer_mass", plummer_mass),
        ("plummer_scale", plummer_scale),
        ("bar_strength", bar_strength),
        ("bar_scale", bar_scale),
        ("bar_tform", bar_tform),
        ("bar_tsteady", bar_tsteady),
        ("bar_pattern_speed", bar_pattern_speed),
    ]:
        if val is not None:
            config_fields[name] = val

    config = PotentialConfig(**config_fields)

    console.print(f"[bold]Integrating {n_particles} orbits...[/bold]")

    result = compute_invariants(config, r_cyl, vr, vt, z, vz, phi, times, delta=delta)
    comparison = compare_variances(result)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "simulation.npz"

    np.savez(
        out_path,
        c2=result.c2,
        jr=result.jr,
        time=result.time,
        var_c2=comparison.var_c2,
        var_jr=comparison.var_jr,
        ratio=comparison.ratio,
        median_ratio=np.array(comparison.median_ratio),
        n_particles=np.array(n_particles),
        r_min=np.array(r_min),
        r_max=np.array(r_max),
        t_end=np.array(t_end),
        n_steps=np.array(n_steps),
        delta=np.array(delta),
        seed=np.array(seed),
        smbh_mass=np.array(config.smbh_mass),
        plummer_mass=np.array(config.plummer_mass),
        plummer_scale=np.array(config.plummer_scale),
        bar_strength=np.array(config.bar_strength),
        bar_scale=np.array(config.bar_scale),
        bar_tform=np.array(config.bar_tform),
        bar_tsteady=np.array(config.bar_tsteady),
        bar_pattern_speed=np.array(config.bar_pattern_speed),
    )

    console.print(f"Saved: {out_path}")
    console.print(f"Median Var(C2)/Var(JR): {comparison.median_ratio:.6e}")
