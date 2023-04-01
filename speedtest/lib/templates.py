# -*- coding: utf-8 -*-
import json
import logging
import os

from dateutil import parser
from jinja2 import Environment, FileSystemLoader, exceptions


logger = logging.getLogger(__name__)


def is_template_valid(template_path: str) -> bool:
    """
    Checks whether a Jinja2 template file exists.

    Args:
        template_path (str): The path to the Jinja2 template file.

    Returns:
        bool: True if the template exists, False otherwise.
    """

    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    try:
        env.get_template(template_file)
    except exceptions.TemplateNotFound:
        return False
    return True


def render_template(template_path: str, data: dict) -> str:
    """
    Renders a Jinja2 template file with the provided data.

    Args:
        template_path (str): The path to the Jinja2 template file.
        data (dict): The data to use when rendering the template.

    Returns:
        str: The rendered template as a string.
    """
    env = Environment(loader=FileSystemLoader('.'))
    env.globals.update(parser=parser)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.strip_trailing_newlines = True

    template = env.get_template(template_path)
    rendered_template = template.render(jsondata=data)

    return rendered_template


def main(data: dict, tpl_path: str):
    """
    Renders a Jinja2 template file with the provided data and returns the rendered output.

    Args:
        data (dict): The data to use when rendering the template.
        tpl_path (str): The path to the Jinja2 template file.

    Returns:
        str: The rendered template as a string.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info('Checking data...')
    if not isinstance(data, dict):
        logger.info('Data format is incorrect. Expected a dictionary.')
        return None

    if not data:
        logger.info('No data provided...')
        return None

    logger.info('Checking template...')
    if not is_template_valid(tpl_path):
        logger.info('Template does not exist...')
        return None
    print(json.dumps(data, indent=4))
    rendered_template = render_template(tpl_path, data)

    return rendered_template


if __name__ == '__main__':
    main()
