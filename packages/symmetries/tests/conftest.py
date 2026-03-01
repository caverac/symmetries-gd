"""Shared fixtures for the symmetries test suite."""

from __future__ import annotations

import numpy as np
import pytest
from symmetries._types import PotentialConfig


@pytest.fixture()
def default_config() -> PotentialConfig:
    """Return a default PotentialConfig."""
    return PotentialConfig()


@pytest.fixture()
def circular_pos_vel() -> tuple[np.ndarray, np.ndarray]:
    """Return position and velocity arrays for a circular orbit in the xy-plane."""
    pos = np.array([1.0, 0.0, 0.0])
    vel = np.array([0.0, 1.0, 0.0])
    return pos, vel


@pytest.fixture()
def sample_phase_arrays() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return sample (pos, vel, time) arrays with shape (2, 5, 3) and (5,)."""
    rng = np.random.default_rng(42)
    pos = rng.standard_normal((2, 5, 3))
    vel = rng.standard_normal((2, 5, 3))
    time = np.linspace(0.0, 1.0, 5)
    return pos, vel, time
