"""Plotting utilities and the ``@docs_figure`` decorator."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from experiments._constants import DOCS_IMG_DIR
from matplotlib.axes import Axes
from matplotlib.figure import Figure


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
    ax.tick_params(direction="in", which="both")
    ax.minorticks_on()


def save_figure_if_changed(fig: Figure, path: Path) -> bool:
    """Save *fig* to *path* only when the content has actually changed.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure to save.
    path : Path
        Destination file path.

    Returns
    -------
    bool
        *True* if the file was written (new or changed), *False* if identical.
    """
    import io

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    new_bytes = buf.getvalue()
    new_hash = hashlib.sha256(new_bytes).hexdigest()

    if path.exists():
        old_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if old_hash == new_hash:
            return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(new_bytes)
    return True


def docs_figure(filename: str) -> Callable[[Callable[..., Figure]], Callable[..., Path]]:
    """Decorate a figure-builder so it saves into ``DOCS_IMG_DIR``.

    Parameters
    ----------
    filename : str
        Output filename (e.g. ``"variance-comparison.png"``).

    Returns
    -------
    Callable
        Decorator that wraps a ``() -> Figure`` into a ``() -> Path``.
    """

    def decorator(fn: Callable[..., Figure]) -> Callable[..., Path]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Path:
            fig = fn(*args, **kwargs)
            dest = DOCS_IMG_DIR / filename
            save_figure_if_changed(fig, dest)
            plt.close(fig)
            return dest

        return wrapper

    return decorator
