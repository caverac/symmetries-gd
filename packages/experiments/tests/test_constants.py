"""Tests for shared constants."""

from __future__ import annotations

from pathlib import Path

from experiments._constants import (
    DEFAULT_LIMIT_N_PARTICLES,
    DEFAULT_LIMIT_THRESHOLD,
    DEFAULT_N_PARTICLES,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_T_END,
    DOCS_IMG_DIR,
    KPC_TO_KM,
    TIME_UNIT_GYR,
)


class TestConstants:
    """Tests for shared constants."""

    def test_docs_img_dir_is_path(self) -> None:
        """Verify DOCS_IMG_DIR is a Path instance."""
        assert isinstance(DOCS_IMG_DIR, Path)

    def test_defaults_types(self) -> None:
        """Verify all default constants have the expected types."""
        assert isinstance(DEFAULT_N_PARTICLES, int)
        assert isinstance(DEFAULT_R_MIN, float)
        assert isinstance(DEFAULT_R_MAX, float)
        assert isinstance(DEFAULT_T_END, float)
        assert isinstance(DEFAULT_N_STEPS, int)
        assert isinstance(DEFAULT_SEED, int)
        assert isinstance(DEFAULT_LIMIT_THRESHOLD, float)
        assert isinstance(DEFAULT_LIMIT_N_PARTICLES, int)
        assert isinstance(KPC_TO_KM, float)
        assert isinstance(TIME_UNIT_GYR, float)
        assert 0.03 < TIME_UNIT_GYR < 0.04  # ~35.6 Myr
