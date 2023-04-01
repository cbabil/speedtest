# -*- coding: utf-8 -*-
import json
import logging

from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError, ValidationError


logger = logging.getLogger(__name__)


def get_schema(schema_file):
    """
    Given a path to a schema file, this function
    reads the schema and returns it as a JSON object.

    Parameters:
    - schema_file: str: Path to the schema file.

    Returns:
    - schema: obj or None: The schema as a JSON object,
                             or None if the file could not be found.
    """
    try:
        logger.info('Using schema file: {}'.format(schema_file))
        with open(schema_file, 'r') as file:
            schema = json.load(file)
            if not schema:
                logger.error('Schema is empty...')
                return None
            return schema
    except FileNotFoundError as err:
        logger.error('Schema not found...')
        logger.error(err)
    except TypeError as err:
        logger.error('Schema error...')
        logger.error(err)
    return None


def validate_schema(schema):
    """
    Validate a JSON schema against the JSON Schema Draft 7 specification.

    Args:
        schema (dict): The JSON schema to validate.

    Returns:
        bool: True if the schema is valid, False otherwise.
    """
    logger.info('Validating schema...')
    try:
        if not schema:
            logger.error('Schema is empty...')
        else:
            # create a FormatChecker instance
            # format_checker = FormatChecker()
            Draft7Validator.check_schema(schema)
            # Use the validate function with additional_properties=False
            # validate(schema, format_checker=format_checker, additional_properties=False)
            return True
    except (ValidationError, SchemaError) as e:
        logger.error(f'Schema validation error: {e}')
    return False
