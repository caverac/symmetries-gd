"""Plotting utilities and the ``@docs_figure`` decorator."""

from __future__ import annotations

import functools
import io
from pathlib import Path
from typing import Any, Callable, TypeVar

import matplotlib.pyplot as plt
import numpy as np
from experiments._console import console
from experiments._constants import DOCS_IMG_DIR
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator

F = TypeVar("F", bound=Callable[..., Figure])

SAVEFIG_DEFAULTS: dict[str, int | str] = {
    "dpi": 300,
    "bbox_inches": "tight",
    "facecolor": "white",
    "edgecolor": "none",
}


def paper_style() -> dict[str, Any]:
    """Return matplotlib rcParams for MNRAS-like figures.

    Returns
    -------
    dict[str, Any]
        Dictionary of matplotlib rcParams.
    """
    return {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.figsize": (4.5, 4.0),
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "lines.linewidth": 1.0,
        "lines.markersize": 3,
    }


def configure_axes(ax: Axes, *, log: bool = False) -> None:
    """Apply consistent styling to a matplotlib axes.

    Parameters
    ----------
    ax : Axes
        The axes to configure.
    log : bool
        If *True*, set both axes to log scale.
    """
    if log:
        ax.set_xscale("log")
        ax.set_yscale("log")
    if ax.get_xscale() == "linear":
        ax.xaxis.set_minor_locator(AutoMinorLocator())
    if ax.get_yscale() == "linear":
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which="minor", length=3, color="gray", direction="in")
    ax.tick_params(which="major", length=6, direction="in")
    ax.tick_params(top=True, right=True, which="both")


def save_figure_if_changed(
    fig: Figure,
    path: Path,
    **savefig_kwargs: Any,
) -> bool:
    """Save a figure only if its pixel content differs from the existing file.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure to save.
    path : Path
        Output path for the figure.
    **savefig_kwargs : Any
        Arguments passed to ``fig.savefig()``.

    Returns
    -------
    bool
        True if the file was written, False if skipped (unchanged).
    """
    if path.exists():
        buf = io.BytesIO()
        fig.savefig(buf, format="png", **savefig_kwargs)
        buf.seek(0)
        new_img = plt.imread(buf)
        existing_img = plt.imread(path)
        if new_img.shape == existing_img.shape and bool(np.array_equal(new_img, existing_img)):
            return False

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, **savefig_kwargs)
    return True


def docs_figure(filename: str, **extra_kwargs: Any) -> Callable[[F], F]:
    """Save the returned Figure to DOCS_IMG_DIR if changed.

    The decorated function must return a ``matplotlib.figure.Figure``.

    Parameters
    ----------
    filename : str
        Output filename (e.g. ``"potential-profile.png"``).
    **extra_kwargs : Any
        Extra arguments forwarded to ``fig.savefig()``.
    """
    savefig_kwargs = {**SAVEFIG_DEFAULTS, **extra_kwargs}

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Figure:
            fig = func(*args, **kwargs)
            path = Path(DOCS_IMG_DIR) / filename
            if save_figure_if_changed(fig, path, **savefig_kwargs):
                console.print(f"  Saved [blue]{path}[/blue]")
            else:
                console.print(f"  Unchanged [dim]{path}[/dim]")
            plt.close(fig)
            return fig

        return wrapper  # type: ignore[return-value]

    return decorator
