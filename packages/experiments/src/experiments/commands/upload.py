"""Upload simulation database to S3."""

import boto3
import click


@click.command()
@click.option("--environment", default="production", help="AWS environment.")
@click.option("--key", default="simulations.db", help="S3 object key.")
@click.option("--src", type=click.Path(exists=True), default="simulations.db", help="Local file to upload.")
def upload(environment: str, key: str, src: str) -> None:
    """Upload simulation database to S3."""
    bucket = f"symmetries-gd-{environment}"
    s3_client = boto3.client("s3")
    s3_client.upload_file(src, bucket, key)
    click.echo(f"Uploaded {src} -> s3://{bucket}/{key}")
