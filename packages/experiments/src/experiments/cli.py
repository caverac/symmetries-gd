"""Click-based CLI entry point."""

import click
from experiments.commands.simulate import simulate
from experiments.commands.variance_plot import variance_plot


@click.group()
def main() -> None:
    """Research CLI for symmetries simulations and paper figures."""


main.add_command(simulate)
main.add_command(variance_plot)
