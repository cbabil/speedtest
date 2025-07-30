# -*- coding: utf-8 -*-
import json
import logging
import shutil
import subprocess

from collections import namedtuple

import click

from codetiming import Timer

import speedtest.lib.templates as templates

from speedtest.config import setup_logging
from speedtest.lib.schemas import get_schema, validate_schema
from speedtest.lib.speedtest import validate_json


logger = logging.getLogger(__name__)


@Timer(
    name='Run Speedtest',
    text='{name} finished in {:.4f} seconds...',
    logger=logging.info,
)
def run_speedtest():
    Result = namedtuple('Result', ['msg', 'err', 'out'])
    logger.info('Running speedtest...')
    speedtest = subprocess.run(
        [
            'speedtest',
            '--accept-license',
            '--accept-gdpr',
            '--selection-details',
            '-f',
            'json',
        ],
        capture_output=True,
    )

    if speedtest.returncode == 0:
        msg = 'Speedtest ran successfully...'
        err = None
        out = speedtest.stdout
    else:
        msg = 'Speedtest failed...'
        err = speedtest.stderr
        out = speedtest.stdout
    return Result(msg, err, out)


def locate(cmd):
    """Returns the path for a given binary

    Args:
        cmd (str): the binary

    Returns:
        path (str): path of given binary if found
    """
    path = shutil.which(cmd, path=None)
    if path:
        return path
    return None


def write_data(data, destination='stdout'):
    """
    Print data to a specified destination or to standard output if no destination is provided.

    Args:
    - data (str): The data to print.
    - destination (str, optional): The destination for the data. Can be a file path
                                   or 'stdout' for standard output. Defaults to 'stdout'.

    Returns:
    - None
    """
    if destination == 'stdout':
        print(data)
    else:
        with open(destination, 'w') as f:
            f.write(data)


def get_template_path(template_name):
    """Get the path to a template file."""
    return f'./speedtest/templates/{template_name}.tpl'


def process_speedtest_data(template, schema_path, output):
    """Run speedtest, validate data, and write to output."""
    setup_logging('INFO')

    if not locate('speedtest'):
        logger.error('Unable to find speedtest. Is it installed?')
        raise FileNotFoundError('speedtest binary not found.')

    logger.info('Output is set to: %s', output)

    tpl_path = get_template_path(template)
    if not templates.is_template_valid(tpl_path):
        logger.error('Invalid template: %s', tpl_path)
        raise ValueError('Invalid template.')

    schema = get_schema(schema_path)
    if not schema or not validate_schema(schema):
        logger.error('Invalid schema: %s', schema_path)
        raise ValueError('Invalid schema.')

    logger.info('Schema is valid...')

    test_result = run_speedtest()

    if not test_result.out:
        logger.error('Speedtest failed: %s', test_result.err.decode('utf-8'))
        raise RuntimeError('Speedtest execution failed.')

    json_data = json.loads(test_result.out)
    is_valid, _ = validate_json(json_data, schema)

    if not is_valid:
        logger.error('JSON data validation failed.')
        raise ValueError('JSON data validation failed.')

    logger.info('JSON data validation successful...')
    data_to_write = templates.main(json_data, tpl_path)
    write_data(data_to_write, output)
    logger.info('Done writing data to %s', output)


@click.command()
@click.option(
    '--template', default='json', show_default=True, help='Template to be used'
)
@click.option(
    '--schema',
    default='speedtest/schemas/schemaV1.json',
    show_default=True,
    help='Speedtest schema',
)
@click.option('--out', default='stdout', show_default=True, help='Output for the data')
@click.option('--loglevel', default='INFO', show_default=True, help='Log Level')
def main(template, schema, out, loglevel):
    """
    Speedtest CLI Data Logger
    """
    try:
        process_speedtest_data(template, schema, out)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(e)
        exit(1)


if __name__ == '__main__':
    main()
