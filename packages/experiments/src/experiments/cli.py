"""Click-based CLI entry point."""

import click
from experiments.commands.action_scatter import action_scatter
from experiments.commands.delta_plot import delta_plot
from experiments.commands.download import download
from experiments.commands.limit_test import limit_test
from experiments.commands.migration_plot import migration_plot
from experiments.commands.migration_scatter import migration_scatter
from experiments.commands.potential_plot import potential_plot
from experiments.commands.simulate import simulate
from experiments.commands.upload import upload


@click.group()
def main() -> None:
    """Research CLI for symmetries simulations and paper figures."""


main.add_command(action_scatter)
main.add_command(delta_plot)
main.add_command(migration_plot)
main.add_command(migration_scatter)
main.add_command(potential_plot)
main.add_command(simulate)
main.add_command(limit_test)
main.add_command(download)
main.add_command(upload)
