# -*- coding: utf-8 -*-
import pytest

from speedtest.lib.speedtest import validate_json


@pytest.mark.usefixtures('valid_schema')
def test_validate_json_valid_data(valid_schema):
    """Test the function with valid JSON data and a valid JSON Schema.

    This test should pass if the function correctly returns the JSON data and True.
    """
    json_data = {'name': 'bar', 'age': 123, 'email': 'bar@testemail.org'}
    result, valid = validate_json(json_data, valid_schema)
    assert result == json_data
    assert valid is True


def test_validate_json_invalid_data():
    """Test the function with invalid JSON data and a valid JSON Schema.

    This test should pass if the function correctly returns None and False.
    """
    json_data = {'foo': 123, 'baz': 'qux'}
    schema = {
        'type': 'object',
        'properties': {'foo': {'type': 'string'}, 'baz': {'type': 'integer'}},
    }
    result, valid = validate_json(json_data, schema)
    assert result is None
    assert valid is False


def test_validate_json_valid_data_invalid_schema():
    """Test the function with valid JSON data and an invalid JSON Schema.

    This test should pass if the function correctly returns None and False.
    """
    json_data = {'foo': 'bar', 'baz': 123}
    schema = {
        'type': 'object',
        'properties': {'foo': {'type': 'string'}, 'baz': {'type': 'string'}},
    }
    result, valid = validate_json(json_data, schema)
    assert result is None
    assert valid is False


@pytest.mark.usefixtures('invalid_schema')
def test_validate_json_invalid_data_invalid_schema(invalid_schema):
    """Test the function with invalid JSON data and an invalid JSON Schema.

    This test should pass if the function correctly returns None and False.
    """
    json_data = {'name': 123, 'age': 'qux', 'email': 'qux@testmail.org'}
    result, valid = validate_json(json_data, invalid_schema)
    assert result is None
    assert valid is False
