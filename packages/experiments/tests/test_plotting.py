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
    """Tests for the configure_axes helper."""

    def test_linear(self) -> None:
        """Verify default axes use linear scale."""
        fig, ax = plt.subplots()
        configure_axes(ax)
        assert ax.get_xscale() == "linear"
        assert ax.get_yscale() == "linear"
        plt.close(fig)

    def test_log(self) -> None:
        """Verify log=True switches both axes to log scale."""
        fig, ax = plt.subplots()
        configure_axes(ax, log=True)
        assert ax.get_xscale() == "log"
        assert ax.get_yscale() == "log"
        plt.close(fig)


class TestSaveFigureIfChanged:
    """Tests for the save_figure_if_changed helper."""

    def test_new_file(self, tmp_path: Path) -> None:
        """Verify a new file is written and returns True."""
        fig = _make_figure()
        path = tmp_path / "test.png"
        assert save_figure_if_changed(fig, path) is True
        assert path.exists()
        plt.close(fig)

    def test_unchanged(self, tmp_path: Path) -> None:
        """Verify an identical figure returns False and does not overwrite."""
        fig = _make_figure()
        path = tmp_path / "test.png"
        save_figure_if_changed(fig, path)
        plt.close(fig)

        fig2 = _make_figure()
        assert save_figure_if_changed(fig2, path) is False
        plt.close(fig2)

    def test_changed(self, tmp_path: Path) -> None:
        """Verify a different figure returns True and overwrites the file."""
        fig = _make_figure()
        path = tmp_path / "test.png"
        save_figure_if_changed(fig, path)
        plt.close(fig)

        fig2, ax2 = plt.subplots()
        ax2.plot([0, 1], [0, 1])
        assert save_figure_if_changed(fig2, path) is True
        plt.close(fig2)

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Verify missing parent directories are created automatically."""
        fig = _make_figure()
        path = tmp_path / "sub" / "dir" / "test.png"
        assert save_figure_if_changed(fig, path) is True
        assert path.exists()
        plt.close(fig)


class TestDocsFigure:
    """Tests for the docs_figure decorator."""

    def test_decorator(self, docs_img_dir: Path) -> None:
        """Verify the decorator saves the figure and returns its path."""

        @docs_figure("test-output.png")
        def build() -> Figure:
            return _make_figure()

        dest = build()
        assert dest == docs_img_dir / "test-output.png"
        assert dest.exists()
