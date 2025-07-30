# -*- coding: utf-8 -*-
# fixtures.py
import io
import logging

import pytest


@pytest.fixture(scope='module')
def caplog():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)
    yield stream
    logger.removeHandler(handler)
    handler.close()


@pytest.fixture(scope='module')
def schema_file():
    """Fixture that open a JSON schema file for testing."""
    schema_file = 'speedtest/schemas/schemaV1.json'
    yield schema_file


@pytest.fixture(scope='module')
def valid_schema():
    yield {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'title': 'Schema Example',
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
            'age': {
                'type': 'integer',
            },
            'email': {
                'type': 'string',
            },
        },
        'required': ['name', 'age', 'email'],
    }


@pytest.fixture(scope='module')
def invalid_schema():
    yield {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'title': 'Schema Example',
        'type': 'object',
        'required': ['name', 'age', 'email'],
        'properties': {
            'name': {
                'type': 'string',
            },
            'age': {
                'type': 'integer',
            },
            'email': {
                'type': 'float',
            },  # Should be string
        },
    }


@pytest.fixture(scope='module')
def valid_json_data():
    yield {'name': 'John Doe', 'age': 30, 'email': 'johndoe@example.com'}


@pytest.fixture(scope='module')
def invalid_json_data():
    return {'name': 123, 'age': 'thirty', 'email': 'not an email'}
