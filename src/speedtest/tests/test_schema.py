# -*- coding: utf-8 -*-
import pytest

from speedtest.lib.schemas import get_schema, validate_schema


@pytest.mark.usefixtures('schema_file')
def test_get_schema_valid_file(schema_file: str):
    """Test the get_schema function when the schema file is found"""
    schema = get_schema(schema_file)
    assert isinstance(schema, dict)


@pytest.mark.usefixtures('caplog')
def test_get_schema_invalid_file(caplog):
    """
    Test that get_schema logs an error message when given an invalid file path.
    """
    schema_file = 'nonexistent_file.json'
    schema = get_schema(schema_file)
    assert schema is None
    assert 'Schema not found...' in caplog.getvalue()


def test_get_schema_empty_file_path():
    """
    Test that get_schema returns None when given an empty file path.
    """
    schema_file = ''
    schema = get_schema(schema_file)
    assert schema is None


@pytest.mark.usefixtures('invalid_schema')
def test_validate_schema_invalid(invalid_schema):
    """
    Test the validate_schema function to ensure it correctly
    returns False for invalid JSON schemas against the JSON Schema Draft 7 specification.
    """
    assert validate_schema(invalid_schema) is False


@pytest.mark.usefixtures('valid_schema')
def test_validate_schema_valid(valid_schema):
    """
    Test the validate_schema function to ensure it correctly
    returns True for valid JSON schemas against the JSON Schema Draft 7 specification.
    """
    assert validate_schema(valid_schema) is True


def test_validate_schema_empty_schema():
    """
    Test that validate_schema returns False when given an empty schema.
    """
    empty_schema = {}
    assert validate_schema(empty_schema) is False


def test_validate_schema_invalid_type():
    """
    Test that validate_schema returns False when given a schema with invalid type field.
    """
    invalid_type_schema = {'type': 'invalid'}
    assert validate_schema(invalid_type_schema) is False


def test_validate_schema_invalid_format():
    """
    Test that validate_schema returns False when given a schema with invalid format field.
    """
    invalid_format_schema = {'type': 'string', 'format': 1}
    assert validate_schema(invalid_format_schema) is False


def test_validate_schema_invalid_pattern():
    """
    Test that validate_schema returns False when given a schema with invalid pattern fields.
    """
    invalid_pattern_schema = {'type': 'string', 'pattern': '('}
    assert validate_schema(invalid_pattern_schema) is False
