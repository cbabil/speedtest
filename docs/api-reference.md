# API Reference

This document provides detailed API reference for the speedtest CLI data logger modules.

## speedtest.lib.schemas

### get_schema(schema_file: str) -> Optional[Dict[str, Any]]

Reads and loads a JSON schema file.

**Parameters:**
- `schema_file` (str): Path to the JSON schema file

**Returns:**
- `dict` or `None`: The loaded schema as a dictionary, or None if error

**Example:**
```python
from speedtest.lib.schemas import get_schema

schema = get_schema('speedtest/schemas/schemaV1.json')
if schema:
    print("Schema loaded successfully")
```

### validate_schema(schema: Dict[str, Any]) -> bool

Validates a JSON schema against JSON Schema Draft 7 specification with additional regex pattern validation.

**Parameters:**
- `schema` (dict): The JSON schema to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Features:**
- JSON Schema Draft 7 compliance checking
- Regex pattern validation for `pattern` fields
- Detailed error logging

**Example:**
```python
from speedtest.lib.schemas import validate_schema

schema = {"type": "string", "pattern": "^[a-z]+$"}
is_valid = validate_schema(schema)  # True

invalid_schema = {"type": "string", "pattern": "("}
is_valid = validate_schema(invalid_schema)  # False
```

## speedtest.lib.speedtest

### validate_json(json_data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[Any, bool]

Validates JSON data against a schema and automatically removes invalid fields.

**Parameters:**
- `json_data` (dict): The JSON data to validate
- `schema` (dict): The JSON schema for validation

**Returns:**
- `tuple`: (cleaned_data, is_valid) where cleaned_data is the data with invalid fields removed

**Features:**
- Automatic invalid field removal
- Detailed validation error logging
- Path-based error reporting

**Example:**
```python
from speedtest.lib.speedtest import validate_json

data = {
    "type": "result",
    "ping": {"latency": 15.5, "jitter": 1.2},
    "invalid_field": "will be removed"
}

cleaned_data, is_valid = validate_json(data, schema)
```

## speedtest.lib.templates

### is_template_valid(template_path: str) -> bool

Checks if a Jinja2 template file exists and is valid.

**Parameters:**
- `template_path` (str): Path to the template file

**Returns:**
- `bool`: True if template exists and is valid, False otherwise

**Example:**
```python
from speedtest.lib.templates import is_template_valid

if is_template_valid('speedtest/templates/json.tpl'):
    print("Template is valid")
```

### render_template(template_path: str, data: dict) -> str

Renders a Jinja2 template with provided data.

**Parameters:**
- `template_path` (str): Path to the template file
- `data` (dict): Data to pass to the template

**Returns:**
- `str`: Rendered template output

**Template Environment:**
- `trim_blocks = True`
- `lstrip_blocks = True`
- `strip_trailing_newlines = True`
- Access to `parser` for date parsing

**Example:**
```python
from speedtest.lib.templates import render_template

data = {"timestamp": "2023-12-07T10:30:00Z", "ping": {"latency": 15.5}}
output = render_template('speedtest/templates/json.tpl', data)
```

### main(data: dict, tpl_path: str) -> Optional[str]

High-level function to render a template with validation and error handling.

**Parameters:**
- `data` (dict): Data to render
- `tpl_path` (str): Path to template file

**Returns:**
- `str` or `None`: Rendered output or None if error

**Features:**
- Input validation
- Template existence checking
- Comprehensive error handling
- Logging integration

## speedtest.config

### setup_logging(loglevel: str) -> None

Configures the logging system for the application.

**Parameters:**
- `loglevel` (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

**Configuration:**
- Format: `%(asctime)s - %(name)s - [%(levelname)s] - %(message)s`
- Default level: INFO if not specified

**Example:**
```python
from speedtest.config import setup_logging

setup_logging('DEBUG')
```

## CLI Interface

### Main Entry Point

```bash
python -m speedtest [OPTIONS]
```

**Options:**
- `--template TEXT`: Template to use (default: json)
- `--schema TEXT`: Schema file path (default: speedtest/schemas/schemaV1.json)
- `--out TEXT`: Output destination (default: stdout)
- `--loglevel TEXT`: Logging level (default: INFO)

### Template Discovery

Templates are searched in the following order:
1. `./speedtest/templates/{template}.tpl`
2. `speedtest/templates/{template}.tpl`
3. Package installation path
4. `pkg_resources` resource path

### Error Handling

The CLI provides specific exit codes:
- `0`: Success
- `1`: Error (speedtest binary not found, invalid schema, template not found, etc.)

## Environment Variables

Currently, the application does not use environment variables, but all configuration is done through command-line parameters.

## Dependencies

### Core Dependencies

- **click**: CLI framework
- **jsonschema**: JSON schema validation
- **Jinja2**: Template engine
- **python-dateutil**: Date parsing utilities
- **codetiming**: Performance timing

### Development Dependencies

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **flake8**: Code linting
- **isort**: Import sorting
- **pre-commit**: Git hooks

## Error Types

### Schema Validation Errors

- `SchemaError`: Invalid schema structure
- `ValidationError`: Data doesn't match schema
- `re.error`: Invalid regex pattern in schema

### Template Errors

- `TemplateNotFound`: Template file doesn't exist
- `TemplateSyntaxError`: Invalid Jinja2 syntax
- `UndefinedError`: Referenced undefined variable

### Runtime Errors

- `FileNotFoundError`: Schema or template file not found
- `subprocess.CalledProcessError`: Speedtest CLI execution failed
- `json.JSONDecodeError`: Invalid JSON from speedtest CLI

## Examples

### Basic Usage

```python
from speedtest.lib.schemas import get_schema, validate_schema
from speedtest.lib.speedtest import validate_json
from speedtest.lib.templates import main as render_template

# Load and validate schema
schema = get_schema('speedtest/schemas/schemaV1.json')
if not validate_schema(schema):
    raise ValueError("Invalid schema")

# Validate data
data = {...}  # Speedtest JSON data
clean_data, is_valid = validate_json(data, schema)

if is_valid:
    # Render template
    output = render_template(clean_data, 'speedtest/templates/json.tpl')
    print(output)
```

### Custom Schema

```python
custom_schema = {
    "type": "object",
    "properties": {
        "ping": {
            "type": "object", 
            "properties": {
                "latency": {"type": "number", "minimum": 0}
            }
        }
    },
    "required": ["ping"]
}

if validate_schema(custom_schema):
    # Use custom schema...
```