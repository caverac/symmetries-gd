"""Dynamical symmetry breaking in galaxies.

Track phase-space integrals via the algebraic deformation from SO(3)
(spherical bulge) to SO(2) (axial disk) symmetry, using the Staeckel
focal distance as a gauge field.
"""

from symmetries._types import (
    GalpyPotential,
    InitialConditionsConfig,
    InvariantResult,
    PhasePoint,
    PopulationConfig,
    PotentialConfig,
    VarianceComparison,
)
from symmetries.analysis import compare_variances, compute_invariants
from symmetries.initial_conditions import sample_initial_conditions
from symmetries.invariants import angular_momentum_squared, compute_l_squared, delta_miyamoto_nagai
from symmetries.orbits import GuidingRadiusInterpolator

__version__ = "0.1.0"

__all__ = [
    "GalpyPotential",
    "GuidingRadiusInterpolator",
    "InitialConditionsConfig",
    "InvariantResult",
    "PhasePoint",
    "PopulationConfig",
    "PotentialConfig",
    "VarianceComparison",
    "__version__",
    "angular_momentum_squared",
    "compare_variances",
    "compute_invariants",
    "compute_l_squared",
    "delta_miyamoto_nagai",
    "sample_initial_conditions",
]
