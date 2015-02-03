import logging
from datetime import datetime, date

import click

from ..utils import get_driver, configure_log
from ..settings import DRIVER_PATH

now = datetime.now()
logger = logging.getLogger(__name__)


@click.group()
@click.option('--logging', default='INFO', help='Logging level.')
@click.pass_context
def main(ctx, logging):
    ctx.obj = {}
    ctx.obj['driver_path'] = DRIVER_PATH
    configure_log(logging)


@main.command()
@click.option(
    '--username', prompt=True, help='Your Chase bank online username.')
@click.option(
    '--password', prompt=True, hide_input=True, confirmation_prompt=True,
    help='Your Chase bank online password.'
)
@click.option(
    '--account_type', type=click.Choice(['cc', 'checking']), default='cc',
    help='The type of account you want data from. Used for traversing different download areas.',
    show_default=True
)
@click.option(
    '--account_id', prompt=True, hide_input=True, confirmation_prompt=True,
    help='Account id. Used to match select boxes on the UI.'
)
@click.option(
    '--from_date', default=date(now.year, now.month, 1).strftime('%m/%d/%Y'),
    help='Transactions from this date.',
    show_default=True
)
@click.option(
    '--to_date', default=now.strftime('%m/%d/%Y'),
    help='Transactions to this date.',
    show_default=True
)
@click.option(
    '--format', type=click.Choice(['QFX', 'CSV']), default='QFX',
    help='Output format of the account export.',
    show_default=True
)
@click.pass_context
def chase(ctx, *args, **kwargs):
    from ..base import ChaseDownloader
    driver_path = ctx.obj['driver_path']
    driver = get_driver(driver_path)

    try:
        chase_downloader = ChaseDownloader(driver, kwargs)
        chase_downloader.run()
    except KeyboardInterrupt:
        driver.close()
    except Exception:
        driver.close()
        raise