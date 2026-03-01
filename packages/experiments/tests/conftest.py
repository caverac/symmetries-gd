"""Shared fixtures for experiments tests."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")


@pytest.fixture()
def simulation_data_dir(tmp_path: Path) -> Path:
    n = 5
    np.savez(
        tmp_path / "simulation.npz",
        c2=np.ones((n, 10)),
        jr=np.ones((n, 10)),
        time=np.linspace(0, 1, 10),
        var_c2=np.full(n, 0.01),
        var_jr=np.full(n, 1.0),
        ratio=np.full(n, 0.01),
        median_ratio=np.array(0.01),
        n_particles=np.array(n),
        r_min=np.array(0.1),
        r_max=np.array(0.3),
        t_end=np.array(2.0),
        n_steps=np.array(100),
        delta=np.array(0.5),
        seed=np.array(42),
    )
    return tmp_path


@pytest.fixture()
def docs_img_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    img_dir = tmp_path / "img"
    img_dir.mkdir()
    monkeypatch.setattr("experiments._constants.DOCS_IMG_DIR", img_dir)
    monkeypatch.setattr("experiments._plotting.DOCS_IMG_DIR", img_dir)
    return img_dir
