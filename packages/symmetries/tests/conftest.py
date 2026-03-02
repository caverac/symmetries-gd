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


def _kepler_ellipse(mu: float, a: float, e: float, n: int = 50) -> tuple[np.ndarray, np.ndarray]:
    """Build pos/vel arrays for n points on a Kepler ellipse."""
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r_vals = a * (1.0 - e**2) / (1.0 + e * np.cos(thetas))
    pos = np.stack(
        [r_vals * np.cos(thetas), r_vals * np.sin(thetas), np.zeros_like(thetas)],
        axis=-1,
    )
    h = np.sqrt(mu * a * (1.0 - e**2))
    v_r = mu * e * np.sin(thetas) / h
    v_theta = h / r_vals
    vx = v_r * np.cos(thetas) - v_theta * np.sin(thetas)
    vy = v_r * np.sin(thetas) + v_theta * np.cos(thetas)
    vel = np.stack([vx, vy, np.zeros_like(thetas)], axis=-1)
    return pos, vel


def _harmonic_orbit(omega: float, a_amp: float, b_amp: float, n: int = 50) -> tuple[np.ndarray, np.ndarray]:
    """Build pos/vel arrays for n points on a 2D harmonic orbit."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = np.stack(
        [a_amp * np.cos(omega * t), b_amp * np.sin(omega * t), np.zeros_like(t)],
        axis=-1,
    )
    vel = np.stack(
        [
            -a_amp * omega * np.sin(omega * t),
            b_amp * omega * np.cos(omega * t),
            np.zeros_like(t),
        ],
        axis=-1,
    )
    return pos, vel


@pytest.fixture()
def kepler_ellipse_default() -> tuple[np.ndarray, np.ndarray]:
    """Return (pos, vel) for a Kepler ellipse with a=2, e=0.3, mu=1."""
    return _kepler_ellipse(mu=1.0, a=2.0, e=0.3)


@pytest.fixture()
def harmonic_orbit_default() -> tuple[np.ndarray, np.ndarray]:
    """Return (pos, vel) for a harmonic orbit with omega=1, A=2, B=1."""
    return _harmonic_orbit(omega=1.0, a_amp=2.0, b_amp=1.0)
