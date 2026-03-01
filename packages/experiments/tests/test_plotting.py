"""Tests for plotting utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from experiments._plotting import configure_axes, docs_figure, save_figure_if_changed
from matplotlib.figure import Figure


def _make_figure() -> Figure:
    fig, _ = plt.subplots()
    return fig


class TestConfigureAxes:
    def test_linear(self) -> None:
        fig, ax = plt.subplots()
        configure_axes(ax)
        assert ax.get_xscale() == "linear"
        assert ax.get_yscale() == "linear"
        plt.close(fig)

    def test_log(self) -> None:
        fig, ax = plt.subplots()
        configure_axes(ax, log=True)
        assert ax.get_xscale() == "log"
        assert ax.get_yscale() == "log"
        plt.close(fig)


class TestSaveFigureIfChanged:
    def test_new_file(self, tmp_path: Path) -> None:
        fig = _make_figure()
        path = tmp_path / "test.png"
        assert save_figure_if_changed(fig, path) is True
        assert path.exists()
        plt.close(fig)

    def test_unchanged(self, tmp_path: Path) -> None:
        fig = _make_figure()
        path = tmp_path / "test.png"
        save_figure_if_changed(fig, path)
        plt.close(fig)

        fig2 = _make_figure()
        assert save_figure_if_changed(fig2, path) is False
        plt.close(fig2)

    def test_changed(self, tmp_path: Path) -> None:
        fig = _make_figure()
        path = tmp_path / "test.png"
        save_figure_if_changed(fig, path)
        plt.close(fig)

        fig2, ax2 = plt.subplots()
        ax2.plot([0, 1], [0, 1])
        assert save_figure_if_changed(fig2, path) is True
        plt.close(fig2)

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        fig = _make_figure()
        path = tmp_path / "sub" / "dir" / "test.png"
        assert save_figure_if_changed(fig, path) is True
        assert path.exists()
        plt.close(fig)


class TestDocsFigure:
    def test_decorator(self, docs_img_dir: Path) -> None:
        @docs_figure("test-output.png")
        def build() -> Figure:
            return _make_figure()

        dest = build()
        assert dest == docs_img_dir / "test-output.png"
        assert dest.exists()
