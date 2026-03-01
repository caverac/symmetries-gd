"""Tests for shared constants."""

from __future__ import annotations

from pathlib import Path

from experiments._constants import (
    DEFAULT_DELTA,
    DEFAULT_N_PARTICLES,
    DEFAULT_N_STEPS,
    DEFAULT_R_MAX,
    DEFAULT_R_MIN,
    DEFAULT_SEED,
    DEFAULT_T_END,
    DOCS_IMG_DIR,
)


class TestConstants:
    def test_docs_img_dir_is_path(self) -> None:
        assert isinstance(DOCS_IMG_DIR, Path)

    def test_defaults_types(self) -> None:
        assert isinstance(DEFAULT_N_PARTICLES, int)
        assert isinstance(DEFAULT_R_MIN, float)
        assert isinstance(DEFAULT_R_MAX, float)
        assert isinstance(DEFAULT_T_END, float)
        assert isinstance(DEFAULT_N_STEPS, int)
        assert isinstance(DEFAULT_DELTA, float)
        assert isinstance(DEFAULT_SEED, int)
