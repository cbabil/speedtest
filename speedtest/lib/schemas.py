# -*- coding: utf-8 -*-
import json
import logging

from typing import Any, Dict, Optional

from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError, ValidationError


logger = logging.getLogger(__name__)


def get_schema(schema_file: str) -> Optional[Dict[str, Any]]:
    """
    Given a path to a schema file, this function
    reads the schema and returns it as a JSON object.

    Parameters:
    - schema_file: str: Path to the schema file.

    Returns:
    - schema: dict or None: The schema as a JSON object,
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


def validate_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate a JSON schema against the JSON Schema Draft 7 specification.

    Args:
        schema (dict): The JSON schema to validate.

    Returns:
        bool: True if the schema is valid, False otherwise.
    """
    import re

    logger.info('Validating schema...')
    try:
        if not schema:
            logger.error('Schema is empty...')
            return False

        # First validate against JSON Schema Draft 7
        Draft7Validator.check_schema(schema)

        # Additional validation for regex patterns
        def validate_patterns(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'pattern' and isinstance(value, str):
                        try:
                            re.compile(value)
                        except re.error as e:
                            logger.error(f'Invalid regex pattern "{value}": {e}')
                            return False
                    elif isinstance(value, (dict, list)):
                        if not validate_patterns(value):
                            return False
            elif isinstance(obj, list):
                for item in obj:
                    if not validate_patterns(item):
                        return False
            return True

        if not validate_patterns(schema):
            return False

        return True
    except (ValidationError, SchemaError) as e:
        logger.error(f'Schema validation error: {e}')
    return False
