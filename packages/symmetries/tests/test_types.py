"""Tests for immutable data containers."""

from __future__ import annotations

import numpy as np
import pytest
from symmetries._types import (
    InitialConditionsConfig,
    InvariantResult,
    PhasePoint,
    PopulationConfig,
    PotentialConfig,
    VarianceComparison,
)


class TestPotentialConfig:
    """Tests for PotentialConfig dataclass."""

    def test_defaults(self) -> None:
        """Verify default parameter values match expected MW-like constants."""
        cfg = PotentialConfig()
        assert cfg.bulge_mass == 0.17
        assert cfg.bulge_scale == 0.0625
        assert cfg.disk_mass == 0.9
        assert cfg.disk_a == 0.375
        assert cfg.disk_b == 0.035
        assert cfg.halo_amp == 3.5
        assert cfg.halo_a == 2.0
        assert cfg.bar_strength == 0.15
        assert cfg.bar_scale == 0.5
        assert cfg.bar_tform == 0.0
        assert cfg.bar_tsteady == 28.0
        assert cfg.bar_pattern_speed == 1.45

    def test_custom_values(self) -> None:
        """Verify custom parameter overrides are stored correctly."""
        cfg = PotentialConfig(bulge_mass=0.2, bulge_scale=0.8)
        assert cfg.bulge_mass == 0.2
        assert cfg.bulge_scale == 0.8

    def test_frozen(self) -> None:
        """Verify frozen dataclass rejects attribute assignment."""
        cfg = PotentialConfig()
        with pytest.raises(AttributeError):
            cfg.bulge_mass = 0.0  # type: ignore[misc]

    def test_slots(self) -> None:
        """Verify slots are enabled for memory efficiency."""
        cfg = PotentialConfig()
        assert hasattr(cfg, "__slots__")


class TestPhasePoint:
    """Tests for PhasePoint dataclass."""

    def test_construction(self, sample_phase_arrays: tuple[np.ndarray, np.ndarray, np.ndarray]) -> None:
        """Verify PhasePoint stores position, velocity, and time arrays."""
        pos, vel, time = sample_phase_arrays
        pp = PhasePoint(pos=pos, vel=vel, time=time)
        assert pp.pos.shape == (2, 5, 3)
        assert pp.vel.shape == (2, 5, 3)
        assert pp.time.shape == (5,)

    def test_frozen(self) -> None:
        """Verify frozen dataclass rejects attribute assignment."""
        pp = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        with pytest.raises(AttributeError):
            pp.pos = np.ones(3)  # type: ignore[misc]

    def test_slots(self) -> None:
        """Verify slots are enabled for memory efficiency."""
        pp = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        assert hasattr(pp, "__slots__")


class TestInvariantResult:
    """Tests for InvariantResult dataclass."""

    def test_construction(self, sample_phase_arrays: tuple[np.ndarray, np.ndarray, np.ndarray]) -> None:
        """Verify InvariantResult stores Jz, Jr, L^2, time, and phase data."""
        pos, vel, time = sample_phase_arrays
        phase = PhasePoint(pos=pos, vel=vel, time=time)
        jz = np.ones((2, 5))
        jr = np.ones((2, 5))
        l_sq = np.ones((2, 5))
        result = InvariantResult(jz=jz, jr=jr, l_sq=l_sq, time=time, phase=phase)
        assert result.jz.shape == (2, 5)
        assert result.jr.shape == (2, 5)
        assert result.l_sq.shape == (2, 5)
        np.testing.assert_array_equal(result.time, time)

    def test_frozen(self) -> None:
        """Verify frozen dataclass rejects attribute assignment."""
        phase = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        result = InvariantResult(jz=np.zeros(1), jr=np.zeros(1), l_sq=np.zeros(1), time=np.zeros(1), phase=phase)
        with pytest.raises(AttributeError):
            result.jz = np.ones(1)  # type: ignore[misc]

    def test_slots(self) -> None:
        """Verify slots are enabled for memory efficiency."""
        phase = PhasePoint(pos=np.zeros(3), vel=np.zeros(3), time=np.zeros(1))
        result = InvariantResult(jz=np.zeros(1), jr=np.zeros(1), l_sq=np.zeros(1), time=np.zeros(1), phase=phase)
        assert hasattr(result, "__slots__")


class TestVarianceComparison:
    """Tests for VarianceComparison dataclass."""

    def test_construction(self) -> None:
        """Verify VarianceComparison stores variance and ratio fields."""
        vc = VarianceComparison(
            var_jz=np.array([0.01]),
            var_jr=np.array([1.0]),
            var_l_sq=np.array([0.05]),
            ratio=np.array([0.01]),
            median_ratio=0.01,
        )
        assert vc.median_ratio == 0.01
        np.testing.assert_array_equal(vc.ratio, np.array([0.01]))

    def test_default_median(self) -> None:
        """Verify median_ratio defaults to zero when not provided."""
        vc = VarianceComparison(
            var_jz=np.array([0.01]),
            var_jr=np.array([1.0]),
            var_l_sq=np.array([0.05]),
            ratio=np.array([0.01]),
        )
        assert vc.median_ratio == 0.0

    def test_frozen(self) -> None:
        """Verify frozen dataclass rejects attribute assignment."""
        vc = VarianceComparison(
            var_jz=np.zeros(1),
            var_jr=np.zeros(1),
            var_l_sq=np.zeros(1),
            ratio=np.zeros(1),
        )
        with pytest.raises(AttributeError):
            vc.median_ratio = 1.0  # type: ignore[misc]

    def test_slots(self) -> None:
        """Verify slots are enabled for memory efficiency."""
        vc = VarianceComparison(
            var_jz=np.zeros(1),
            var_jr=np.zeros(1),
            var_l_sq=np.zeros(1),
            ratio=np.zeros(1),
        )
        assert hasattr(vc, "__slots__")


class TestPopulationConfig:
    """Tests for PopulationConfig dataclass."""

    def test_construction(self) -> None:
        """Verify PopulationConfig stores all fields correctly."""
        pop = PopulationConfig(
            n_particles=50,
            hr=1.0,
            sr=0.2,
            sz=0.1,
            hsr=2.0,
            hsz=2.0,
            r_min=0.5,
            r_max=3.0,
            label="bulge",
        )
        assert pop.n_particles == 50
        assert pop.hr == 1.0
        assert pop.sr == 0.2
        assert pop.sz == 0.1
        assert pop.hsr == 2.0
        assert pop.hsz == 2.0
        assert pop.r_min == 0.5
        assert pop.r_max == 3.0
        assert pop.label == "bulge"

    def test_defaults(self) -> None:
        """Verify z_max and label default values."""
        pop = PopulationConfig(n_particles=10, hr=1.0, sr=0.2, sz=0.1, hsr=2.0, hsz=2.0, r_min=0.1, r_max=1.0)
        assert pop.z_max == 0.05
        assert pop.label == ""

    def test_frozen(self) -> None:
        """Verify frozen dataclass rejects attribute assignment."""
        pop = PopulationConfig(n_particles=10, hr=1.0, sr=0.2, sz=0.1, hsr=2.0, hsz=2.0, r_min=0.1, r_max=1.0)
        with pytest.raises(AttributeError):
            pop.n_particles = 20  # type: ignore[misc]

    def test_slots(self) -> None:
        """Verify slots are enabled for memory efficiency."""
        pop = PopulationConfig(n_particles=10, hr=1.0, sr=0.2, sz=0.1, hsr=2.0, hsz=2.0, r_min=0.1, r_max=1.0)
        assert hasattr(pop, "__slots__")


class TestInitialConditionsConfig:
    """Tests for InitialConditionsConfig dataclass."""

    def test_defaults(self) -> None:
        """Verify default values for populations and seed."""
        ic = InitialConditionsConfig()
        assert not ic.populations
        assert ic.seed == 42

    def test_custom_values(self) -> None:
        """Verify custom population and seed are stored."""
        pop = PopulationConfig(n_particles=10, hr=1.0, sr=0.2, sz=0.1, hsr=2.0, hsz=2.0, r_min=0.1, r_max=1.0)
        ic = InitialConditionsConfig(populations=(pop,), seed=99)
        assert len(ic.populations) == 1
        assert ic.seed == 99

    def test_frozen(self) -> None:
        """Verify frozen dataclass rejects attribute assignment."""
        ic = InitialConditionsConfig()
        with pytest.raises(AttributeError):
            ic.seed = 0  # type: ignore[misc]

    def test_slots(self) -> None:
        """Verify slots are enabled for memory efficiency."""
        ic = InitialConditionsConfig()
        assert hasattr(ic, "__slots__")
