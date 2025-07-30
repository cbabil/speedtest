# -*- coding: utf-8 -*-
import logging

from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError, UndefinedTypeCheck, UnknownType


logger = logging.getLogger(__name__)


def validate_json(json_data, schema):
    """Validate JSON data against a JSON Schema.

    Args:
    - json_data (dict): The JSON data to validate.
    - schema (dict): The JSON Schema to use for validation.

    Returns:
    - tuple: A tuple containing a boolean indicating if the data is valid
             and a list of validation errors.
    """
    try:
        logger.info('Validating JSON data...')
        validator = Draft7Validator(schema)
        errors = sorted(validator.iter_errors(json_data), key=lambda e: e.path)
        if errors:
            logger.error('Validation errors found:')
            for error in errors:
                logger.error(f'{error.message} in path {error.path}')
            return False, errors
        else:
            logger.info('JSON data is valid.')
            return True, []
    except (SchemaError, UndefinedTypeCheck, UnknownType) as e:
        logger.error('Error in the JSON Schema: {}'.format(e))
        return False, [e]
