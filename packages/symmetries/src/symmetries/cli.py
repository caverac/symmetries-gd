"""Command-line interface for symmetries analysis."""

from __future__ import annotations

import argparse
import sys

import numpy as np
from symmetries._types import PotentialConfig
from symmetries.analysis import compare_variances, compute_invariants


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="symmetries",
        description="Compute deformed Casimir invariant C_2 for migrating stars",
    )
    parser.add_argument("-n", "--n-particles", type=int, default=10, help="Number of test particles")
    parser.add_argument("--r-min", type=float, default=0.1, help="Minimum initial radius (kpc)")
    parser.add_argument("--r-max", type=float, default=0.3, help="Maximum initial radius (kpc)")
    parser.add_argument("--t-end", type=float, default=2.0, help="Integration end time (Gyr)")
    parser.add_argument("--n-steps", type=int, default=100, help="Number of time steps")
    parser.add_argument("--delta", type=float, default=0.5, help="Staeckel delta parameter")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser


def run(args: argparse.Namespace) -> None:
    """Execute the analysis pipeline from parsed arguments.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments.
    """
    rng = np.random.default_rng(args.seed)

    r_cyl = rng.uniform(args.r_min, args.r_max, size=args.n_particles)
    vr = np.zeros(args.n_particles)
    vt = np.ones(args.n_particles)
    z = np.zeros(args.n_particles)
    vz = np.zeros(args.n_particles)
    phi = rng.uniform(0, 2 * np.pi, size=args.n_particles)

    times = np.linspace(0.0, args.t_end, args.n_steps)
    config = PotentialConfig()

    result = compute_invariants(config, r_cyl, vr, vt, z, vz, phi, times, delta=args.delta)
    comparison = compare_variances(result)

    print(f"Particles: {args.n_particles}")  # noqa: T201
    print(f"Median Var(C2)/Var(JR): {comparison.median_ratio:.6e}")  # noqa: T201
    print(f"Mean Var(C2):           {float(np.mean(comparison.var_c2)):.6e}")  # noqa: T201
    print(f"Mean Var(JR):           {float(np.mean(comparison.var_jr)):.6e}")  # noqa: T201


def main() -> None:
    """Entry point for the symmetries CLI."""
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    run(args)
