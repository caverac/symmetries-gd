"""Shared constants for the experiments CLI."""

from pathlib import Path

DOCS_IMG_DIR: Path = Path(__file__).resolve().parents[4] / "packages" / "docs" / "static" / "img"

# galpy natural-unit conversion factors
R0_KPC: float = 8.0
"""Solar galactocentric radius in kpc."""

V0_KMS: float = 220.0
"""Circular velocity at the Sun in km/s."""

KPC_TO_KM: float = 3.0857e16
"""1 kpc in km."""

TIME_UNIT_GYR: float = R0_KPC * KPC_TO_KM / V0_KMS / 3.1557e16
"""1 galpy time unit (R0/V0) in Gyr ~ 0.0356 Gyr ~ 35.6 Myr."""

# Defaults used by plot/analysis commands (limit-test, migration-plot)
DEFAULT_N_PARTICLES: int = 200
DEFAULT_R_MIN: float = 0.3
DEFAULT_R_MAX: float = 1.5
DEFAULT_T_END: float = 4.0
DEFAULT_N_STEPS: int = 100
DEFAULT_SEED: int = 42

DEFAULT_LIMIT_THRESHOLD: float = 1e-12
DEFAULT_LIMIT_N_PARTICLES: int = 50
