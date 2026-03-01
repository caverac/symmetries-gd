"""Shared constants for the experiments CLI."""

from pathlib import Path

DOCS_IMG_DIR: Path = Path(__file__).resolve().parents[4] / "docs" / "static" / "img"

DEFAULT_N_PARTICLES: int = 200
DEFAULT_R_MIN: float = 0.1
DEFAULT_R_MAX: float = 0.3
DEFAULT_T_END: float = 2.0
DEFAULT_N_STEPS: int = 100
DEFAULT_DELTA: float = 0.5
DEFAULT_SEED: int = 42
