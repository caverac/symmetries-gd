"""Tests for immutable data containers."""

from __future__ import annotations

import numpy as np
import pytest
from symmetries._types import InvariantResult, PhasePoint, PotentialConfig, VarianceComparison


class TestPotentialConfig:
    def test_defaults(self) -> None:
        cfg = PotentialConfig()
        assert cfg.smbh_mass == 4e6
        assert cfg.plummer_mass == 1e10
        assert cfg.plummer_scale == 0.5
        assert cfg.bar_mass == 1e9
        assert cfg.bar_scale == 1.0
        assert cfg.bar_tform == -5.0
        assert cfg.bar_tsteady == 2.0
        assert cfg.bar_pattern_speed == 40.0

    def test_custom_values(self) -> None:
        cfg = PotentialConfig(smbh_mass=1e7, plummer_mass=2e10)
        assert cfg.smbh_mass == 1e7
        assert cfg.plummer_mass == 2e10

    def test_frozen(self) -> None:
        cfg = PotentialConfig()
        with pytest.raises(AttributeError):
            cfg.smbh_mass = 0.0  # type: ignore[misc]

    def test_slots(self) -> None:
        cfg = PotentialConfig()
        assert hasattr(cfg, "__slots__")


class TestPhasePoint:
    def test_construction(self, sample_phase_arrays: tuple[np.ndarray, np.ndarray, np.ndarray]) -> None:
        pos, vel, time = sample_phase_arrays
        pp = PhasePoint(pos=pos, vel=vel, time=time)
        assert pp.pos.shape == (2, 5, 3)
        assert pp.vel.shape == (2, 5, 3)
        assert pp.time.shape == (5,)

    def test_frozen(self) -> None:
        pp = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        with pytest.raises(AttributeError):
            pp.pos = np.ones(3)  # type: ignore[misc]

    def test_slots(self) -> None:
        pp = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        assert hasattr(pp, "__slots__")


class TestInvariantResult:
    def test_construction(self, sample_phase_arrays: tuple[np.ndarray, np.ndarray, np.ndarray]) -> None:
        pos, vel, time = sample_phase_arrays
        phase = PhasePoint(pos=pos, vel=vel, time=time)
        c2 = np.ones((2, 5))
        jr = np.ones((2, 5))
        result = InvariantResult(c2=c2, jr=jr, time=time, phase=phase)
        assert result.c2.shape == (2, 5)
        assert result.jr.shape == (2, 5)
        np.testing.assert_array_equal(result.time, time)

    def test_frozen(self) -> None:
        phase = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        result = InvariantResult(c2=np.zeros(1), jr=np.zeros(1), time=np.zeros(1), phase=phase)
        with pytest.raises(AttributeError):
            result.c2 = np.ones(1)  # type: ignore[misc]

    def test_slots(self) -> None:
        phase = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        result = InvariantResult(c2=np.zeros(1), jr=np.zeros(1), time=np.zeros(1), phase=phase)
        assert hasattr(result, "__slots__")


class TestVarianceComparison:
    def test_construction(self) -> None:
        vc = VarianceComparison(
            var_c2=np.array([0.01]),
            var_jr=np.array([1.0]),
            ratio=np.array([0.01]),
            median_ratio=0.01,
        )
        assert vc.median_ratio == 0.01
        np.testing.assert_array_equal(vc.ratio, np.array([0.01]))

    def test_default_median(self) -> None:
        vc = VarianceComparison(
            var_c2=np.array([0.01]),
            var_jr=np.array([1.0]),
            ratio=np.array([0.01]),
        )
        assert vc.median_ratio == 0.0

    def test_frozen(self) -> None:
        vc = VarianceComparison(
            var_c2=np.zeros(1),
            var_jr=np.zeros(1),
            ratio=np.zeros(1),
        )
        with pytest.raises(AttributeError):
            vc.median_ratio = 1.0  # type: ignore[misc]

    def test_slots(self) -> None:
        vc = VarianceComparison(
            var_c2=np.zeros(1),
            var_jr=np.zeros(1),
            ratio=np.zeros(1),
        )
        assert hasattr(vc, "__slots__")
