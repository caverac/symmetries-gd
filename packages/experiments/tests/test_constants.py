"""Tests for shared constants."""

from __future__ import annotations

from pathlib import Path

from experiments._constants import (
    DEFAULT_CONV_N_POINTS,
    DEFAULT_CONV_TFORM_MAX,
    DEFAULT_CONV_TFORM_MIN,
    DEFAULT_DELTA,
    DEFAULT_LIMIT_N_PARTICLES,
    DEFAULT_LIMIT_THRESHOLD,
    DEFAULT_N_PARTICLES,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_STRESS_BAR_MAX,
    DEFAULT_STRESS_BAR_MIN,
    DEFAULT_STRESS_N_POINTS,
    DEFAULT_T_END,
    DOCS_IMG_DIR,
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
        assert isinstance(DEFAULT_DELTA, float)
        assert isinstance(DEFAULT_SEED, int)
        assert isinstance(DEFAULT_LIMIT_THRESHOLD, float)
        assert isinstance(DEFAULT_LIMIT_N_PARTICLES, int)
        assert isinstance(DEFAULT_STRESS_BAR_MIN, float)
        assert isinstance(DEFAULT_STRESS_BAR_MAX, float)
        assert isinstance(DEFAULT_STRESS_N_POINTS, int)
        assert isinstance(DEFAULT_CONV_TFORM_MIN, float)
        assert isinstance(DEFAULT_CONV_TFORM_MAX, float)
        assert isinstance(DEFAULT_CONV_N_POINTS, int)
