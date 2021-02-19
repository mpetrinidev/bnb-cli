import click

from src.cli import pass_environment
from src.utils.config import write_credentials, remove_credentials


@click.group(short_help="Add or remove Binance CLI credentials (api_key and secret)")
def cli():
    pass


@cli.command("add", short_help="Add Binance CLI's credentials (api_key and secret) to start using Binance CLI")
@click.option("-ak", "--api_key", required=True, type=click.types.STRING)
@click.option("-s", "--secret", required=True, type=click.types.STRING)
@pass_environment
def add(ctx, api_key: str, secret: str):
    """Add Binance CLI's credentials (api_key and secret) to start using Binance CLI"""
    write_credentials(api_key, secret)
    ctx.log("Binance CLI's credentials added successfully")


@cli.command('remove', short_help="Remove Binance CLI's credentials (api_key and secret)")
@pass_environment
def remove(ctx):
    """Remove Binance CLI's credentials (api_key and secret).

    WARNING: You cannot use Binance CLI again until you add new credentials.
    """
    remove_credentials()

    ctx.log("Binance CLI's credentials removed successfully. \n\nRe-run <bnc credentials add> to start using again "
            "Binance CLI")
