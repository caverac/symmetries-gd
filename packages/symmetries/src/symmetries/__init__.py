"""Dynamical symmetry breaking in galaxies.

Track phase-space integrals via parameterized Lie algebra deformations
between SO(4) (Keplerian) and SU(3) (harmonic) symmetry limits.
"""

from symmetries._types import InvariantResult, PhasePoint, PotentialConfig, VarianceComparison
from symmetries.analysis import compare_variances, compute_invariants, omega_from_plummer
from symmetries.invariants import compute_c2
from symmetries.tensors import (
    angular_momentum_squared,
    fradkin_tensor,
    generalized_tensor,
    lrl_tensor,
    lrl_vector,
    tensor_trace_squared,
)

__version__ = "0.1.0"

__all__ = [
    "InvariantResult",
    "PhasePoint",
    "PotentialConfig",
    "VarianceComparison",
    "__version__",
    "angular_momentum_squared",
    "compare_variances",
    "compute_c2",
    "compute_invariants",
    "fradkin_tensor",
    "generalized_tensor",
    "lrl_tensor",
    "lrl_vector",
    "omega_from_plummer",
    "tensor_trace_squared",
]
