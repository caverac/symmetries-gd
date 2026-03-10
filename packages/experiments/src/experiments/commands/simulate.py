"""Run orbit integration and store results in SQLite."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import click
import numpy as np
from experiments._console import console
from experiments._database import SimulationDB
from experiments._models import RunConfig
from galpy.orbit import Orbit
from galpy.potential import vcirc
from symmetries import GuidingRadiusInterpolator, sample_initial_conditions
from symmetries._types import GalpyPotential, PhasePoint, PotentialConfig
from symmetries.invariants import compute_l_squared, delta_miyamoto_nagai
from symmetries.orbits import cartesian_to_cylindrical, compute_actions
from symmetries.potentials import build_axisymmetric, build_composite

_DT_FRACTION = 0.1


def _integrate_all_orbits(
    r_cyl: np.ndarray,
    vr: np.ndarray,
    vt: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    phi: np.ndarray,
    axisym: list[GalpyPotential],
    composite: list[GalpyPotential],
    snapshot_times: np.ndarray,
    t_end: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate each orbit with a per-particle time step.

    Parameters
    ----------
    r_cyl : ndarray
        Initial cylindrical radii.
    vr : ndarray
        Initial radial velocities.
    vt : ndarray
        Initial tangential velocities.
    z : ndarray
        Initial vertical positions.
    vz : ndarray
        Initial vertical velocities.
    phi : ndarray
        Initial azimuthal angles.
    axisym : list
        Axisymmetric galpy potential (for circular velocity).
    composite : list
        Full composite galpy potential (for orbit integration).
    snapshot_times : ndarray
        Times at which to record snapshots.
    t_end : float
        End time.

    Returns
    -------
    tuple[ndarray, ndarray]
        Cartesian positions and velocities, each ``(n_particles, n_snaps, 3)``.
    """
    import time as _time

    total = len(r_cyl)
    n_snaps = len(snapshot_times)
    pos_all = np.zeros((total, n_snaps, 3))
    vel_all = np.zeros((total, n_snaps, 3))

    t0_total = _time.perf_counter()
    for i in range(total):
        t0_orb = _time.perf_counter()

        vc_i = float(vcirc(axisym, float(r_cyl[i]), use_physical=False))
        t_circ = 2.0 * np.pi * float(r_cyl[i]) / max(vc_i, 1e-30)
        dt = _DT_FRACTION * t_circ

        fine_grid = np.arange(0.0, t_end + dt, dt)
        integration_times = np.union1d(fine_grid, snapshot_times)

        orb = Orbit(vxvv=[r_cyl[i], vr[i], vt[i], z[i], vz[i], phi[i]])
        orb.integrate(integration_times, composite, method="dop853_c")

        pos_all[i, :, 0] = orb.x(snapshot_times)
        pos_all[i, :, 1] = orb.y(snapshot_times)
        pos_all[i, :, 2] = orb.z(snapshot_times)
        vel_all[i, :, 0] = orb.vx(snapshot_times)
        vel_all[i, :, 1] = orb.vy(snapshot_times)
        vel_all[i, :, 2] = orb.vz(snapshot_times)

        elapsed = _time.perf_counter() - t0_orb
        console.print(
            f"  [dim]Orbit {i + 1}/{total}: R={float(r_cyl[i]):.3f} "
            f"Vc={vc_i:.3f} dt={dt:.4f} n_int={len(integration_times)} "
            f"t={elapsed:.2f}s[/dim]"
        )
    console.print(f"  [dim]Integration total: {_time.perf_counter() - t0_total:.1f}s[/dim]")
    return pos_all, vel_all


def _build_snapshot_rows(
    total: int,
    n_snaps: int,
    snapshot_times: np.ndarray,
    r_all: np.ndarray,
    vr_all: np.ndarray,
    vt_all: np.ndarray,
    z_all: np.ndarray,
    vz_all: np.ndarray,
    phi_all: np.ndarray,
    jr_all: np.ndarray,
    lz_all: np.ndarray,
    jz_all: np.ndarray,
    l_sq_all: np.ndarray,
    rg_all: np.ndarray,
    labels: np.ndarray,
) -> list[tuple[object, ...]]:
    """Assemble snapshot rows for database insertion.

    Parameters
    ----------
    total : int
        Number of particles.
    n_snaps : int
        Number of time snapshots.
    snapshot_times : ndarray
        Snapshot time array.
    r_all : ndarray
        Cylindrical radii, shape ``(total, n_snaps)``.
    vr_all : ndarray
        Radial velocities.
    vt_all : ndarray
        Tangential velocities.
    z_all : ndarray
        Vertical positions.
    vz_all : ndarray
        Vertical velocities.
    phi_all : ndarray
        Azimuthal angles.
    jr_all : ndarray
        Radial actions.
    lz_all : ndarray
        Angular momenta.
    jz_all : ndarray
        Vertical actions.
    l_sq_all : ndarray
        Squared total angular momentum.
    rg_all : ndarray
        Guiding radii.
    labels : ndarray
        Population labels per particle.

    Returns
    -------
    list[tuple[object, ...]]
        Rows ready for ``SimulationDB.insert_snapshots``.
    """
    rows: list[tuple[object, ...]] = []
    for p in range(total):
        lab = int(labels[p])
        for t_idx in range(n_snaps):
            rows.append(
                (
                    p,
                    float(snapshot_times[t_idx]),
                    float(r_all[p, t_idx]),
                    float(vr_all[p, t_idx]),
                    float(vt_all[p, t_idx]),
                    float(z_all[p, t_idx]),
                    float(vz_all[p, t_idx]),
                    float(phi_all[p, t_idx]),
                    float(jr_all[p, t_idx]),
                    float(lz_all[p, t_idx]),
                    float(jz_all[p, t_idx]),
                    float(l_sq_all[p, t_idx]),
                    float(rg_all[p, t_idx]),
                    lab,
                )
            )
    return rows


def _compute_derived_quantities(
    pos_all: np.ndarray,
    vel_all: np.ndarray,
    snapshot_times: np.ndarray,
    pot_config: PotentialConfig,
    axisym: list[GalpyPotential],
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Compute cylindrical coords, actions, L^2, and guiding radii from Cartesian phase space.

    Parameters
    ----------
    pos_all : ndarray
        Cartesian positions, shape ``(n_particles, n_snaps, 3)``.
    vel_all : ndarray
        Cartesian velocities, shape ``(n_particles, n_snaps, 3)``.
    snapshot_times : ndarray
        Snapshot time array.
    pot_config : PotentialConfig
        Potential configuration (for disk geometry).
    axisym : list[GalpyPotential]
        Axisymmetric galpy potential.

    Returns
    -------
    tuple
        ``(r, vr, vt, z, vz, phi, jr, jz, lz, l_sq, rg)`` arrays.
    """
    import time as _time

    # Cylindrical coordinates
    t0 = _time.perf_counter()
    r_all, vr_all, vt_all, z_all, vz_all, phi_all = cartesian_to_cylindrical(pos_all, vel_all)
    console.print(f"  [dim]Cylindrical conversion: {_time.perf_counter() - t0:.1f}s[/dim]")

    lz_all = r_all * vt_all

    # Staeckel delta
    delta_arr = delta_miyamoto_nagai(r_all, pot_config.disk_a, pot_config.disk_b)
    console.print(
        f"  [dim]Staeckel delta: median={float(np.median(delta_arr)):.4f} "
        f"range=[{float(np.min(delta_arr)):.4f}, {float(np.max(delta_arr)):.4f}][/dim]"
    )

    # Actions
    console.print("[bold]Computing actions (Staeckel Fudge, variable Delta)...[/bold]")
    t0 = _time.perf_counter()
    phase = PhasePoint(pos=pos_all, vel=vel_all, time=snapshot_times)
    jr_all, _lz_act, jz_all = compute_actions(phase, axisym, delta=delta_arr)
    console.print(f"  [dim]Actions: {_time.perf_counter() - t0:.1f}s[/dim]")

    # L^2
    console.print("[bold]Computing L^2...[/bold]")
    t0 = _time.perf_counter()
    l_sq_all = compute_l_squared(pos_all, vel_all)
    console.print(f"  [dim]L^2: {_time.perf_counter() - t0:.1f}s[/dim]")

    # Guiding radii
    console.print("[bold]Computing guiding radii...[/bold]")
    t0 = _time.perf_counter()
    n_snaps = len(snapshot_times)
    rg_interp = GuidingRadiusInterpolator(axisym)
    rg_all = np.zeros_like(lz_all)
    for t_idx in range(n_snaps):
        rg_all[:, t_idx] = rg_interp(lz_all[:, t_idx])
    console.print(f"  [dim]Guiding radii: {_time.perf_counter() - t0:.1f}s[/dim]")

    return r_all, vr_all, vt_all, z_all, vz_all, phi_all, jr_all, jz_all, lz_all, l_sq_all, rg_all


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
        with contextlib.redirect_stdout(io.StringIO()):
            r_cyl, vr, vt, z, vz, phi, labels = sample_initial_conditions(ic_config, pot_config)
        total = len(r_cyl)

        # Potentials
        axisym = build_axisymmetric(pot_config)
        composite = build_composite(pot_config)

        # Snapshot times
        snapshot_times = np.linspace(0.0, config.t_end, config.n_steps)

        # Orbit integration
        console.print(f"[bold]Integrating {total} orbits with per-particle dt...[/bold]")
        pos_all, vel_all = _integrate_all_orbits(
            r_cyl, vr, vt, z, vz, phi, axisym, composite, snapshot_times, config.t_end
        )

        # Derived quantities: cylindrical coords, actions, L^2, guiding radii
        r_all, vr_all, vt_all, z_all, vz_all, phi_all, jr_all, jz_all, lz_all, l_sq_all, rg_all = (
            _compute_derived_quantities(pos_all, vel_all, snapshot_times, pot_config, axisym)
        )

        # Build snapshot rows and store
        n_snaps = len(snapshot_times)
        console.print("[bold]Writing snapshots to database...[/bold]")
        rows = _build_snapshot_rows(
            total,
            n_snaps,
            snapshot_times,
            r_all,
            vr_all,
            vt_all,
            z_all,
            vz_all,
            phi_all,
            jr_all,
            lz_all,
            jz_all,
            l_sq_all,
            rg_all,
            labels,
        )
        db.insert_snapshots(run_id, rows)

        console.print(f"[green]Done.[/green] Run '{name}' (id={run_id}): {total} particles, {n_snaps} snapshots.")
        console.print(f"  Total snapshots: {len(rows)}")
        console.print(f"  Database: {outdir / 'simulations.db'}")
    finally:
        db.close()
