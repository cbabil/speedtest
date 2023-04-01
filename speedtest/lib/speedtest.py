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
    - bool: True if the JSON data is valid, False otherwise.
    """
    while True:
        try:
            logger.info('Validating JSON data...')
            v = Draft7Validator(schema)
            current = json_data
            errors = sorted(v.iter_errors(json_data), key=lambda e: e.path)
            if errors:
                logger.error('Validation errors found:')
                for error in errors:
                    logger.error(f'{error.message} in path {error.path}')
                    path_queue = error.path
                    while path_queue:
                        key = path_queue.popleft()
                        if isinstance(current, dict) and key in current:
                            if not path_queue:
                                logger.info(f'Removing {key} from data')
                                del current[key]
                                break
                            else:
                                current = current[key]
                        elif isinstance(current, list) and isinstance(key, int):
                            key = int(key)
                            if key >= 0 and key < len(current):
                                logger.info(f'Removing current key: {current[key]}')
                                del current[key]
                                break
                            else:
                                raise IndexError(
                                    'Index {} out of range in JSON path'.format(key)
                                )
                        else:
                            raise KeyError('Key {} not found in JSON path'.format(key))
            else:
                logger.info('JSON data is valid.')
                return json_data, True
        except SchemaError as e:
            logger.error('Error in the JSON Schema: {}'.format(e))
        except TypeError as e:
            logger.error('Error in the JSON data: {}'.format(e))
        except IndexError as e:
            logger.error('Error in the JSON data: {}'.format(e))
        except UndefinedTypeCheck as e:
            logger.error('Error in the JSON data: {}'.format(e))
        except UnknownType as e:
            logger.error('Error in the JSON data: {}'.format(e))
        return None, False
