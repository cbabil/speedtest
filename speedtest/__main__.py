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
@click.option(
    '--out',
    default='stdout',
    show_default=True,
    help='Output for the data')
@click.option(
    '--loglevel',
    default='INFO',
    show_default=True,
    help='Log Level')
def main(template, schema, out, loglevel):
    """
    Speedtest CLI Data Logger
    """

    setup_logging(loglevel)

    # Check to ensure that speedtest binary is installed
    speedtestPath = locate('speedtest')
    if speedtestPath is None:
        logger.error('unable to find speedtest. Is it intalled?')
        exit(1)
    else:
        logger.info('found speedtest: %s', speedtestPath)

    if out:
        logger.info('output is set to: %s', out)
        destination = out

    # Check to ensure that the connector is valid
    if template:
        logger.info('using template: %s', template)
        tpl_path = './speedtest/templates/' + template + '.tpl'
        validtpl = templates.is_template_valid(tpl_path)
    else:
        logger.info('missing template....')

    # Check to ensure that the schema file is found
    schema = get_schema(schema)
    if schema is None:
        logger.info('Exiting...')
        exit(1)
    else:
        # validate schema
        valide_schema = validate_schema(schema)
        if valide_schema is False:
            logger.info('Invalid schema. Exiting....')
            exit(1)
        else:
            logger.info('Schema is valid...')

    # running speedtest
    test = run_speedtest()

    # Verifying the integrity of the
    # json output against the schema
    if ((test.out).decode("utf-8")):
        logger.info(test.msg)
        valid_json_data, is_json_valid = validate_json(json.loads(test.out), schema)
        if is_json_valid:
            logger.info('JSON data validation successful...')
            if validtpl:
                data = templates.main(valid_json_data, tpl_path)
                write_data(data, destination)
                logger.info('Done writting data to {}'.format(destination))
        else:
            logger.info('JSON data validation failed. Exiting...')
            exit(1)
    else:
        logger.info(test.msg)
        logger.info((test.err).decode("utf-8"))
        exit(1)


if __name__ == '__main__':
    main()
