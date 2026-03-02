"""Click-based CLI entry point."""

import click
from experiments.commands.convergence import convergence
from experiments.commands.limit_test import limit_test
from experiments.commands.simulate import simulate
from experiments.commands.stress_test import stress_test
from experiments.commands.variance_plot import variance_plot


@click.group()
def main() -> None:
    """Research CLI for symmetries simulations and paper figures."""


main.add_command(simulate)
main.add_command(variance_plot)
main.add_command(limit_test)
main.add_command(stress_test)
main.add_command(convergence)
