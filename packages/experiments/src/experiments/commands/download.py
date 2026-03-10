"""Download simulation database from S3."""

import urllib.request
from pathlib import Path

import click

_DEFAULT_DEST = Path("packages/experiments/data/simulations.db")


@click.command()
@click.option("--environment", default="production", help="AWS environment.")
@click.option("--key", default="simulations.db", help="S3 object key.")
@click.option(
    "--dest",
    type=click.Path(path_type=Path),
    default=_DEFAULT_DEST,
    show_default=True,
    help="Local destination.",
)
def download(environment: str, key: str, dest: Path) -> None:
    """Download simulation database from S3."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    bucket = f"symmetries-gd-{environment}"
    url = f"https://{bucket}.s3.amazonaws.com/{key}"
    urllib.request.urlretrieve(url, dest)  # noqa: S310
    click.echo(f"Downloaded s3://{bucket}/{key} -> {dest}")
