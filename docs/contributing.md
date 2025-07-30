# Contributing Guide

Thank you for your interest in contributing to the speedtest CLI data logger! This guide will help you get started.

## Development Setup

### Prerequisites

1. Python 3.8 or higher
2. Git
3. Ookla Speedtest CLI (for testing)

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/cbabil/speedtest.git
cd speedtest

# Install in development mode
pip install -e .

# Install development dependencies
pip install flake8 isort pre-commit black

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest speedtest/tests/ -v

# Run with coverage
pytest speedtest/tests/ --cov=speedtest --cov-report=html

# Run specific test file
pytest speedtest/tests/test_schema.py -v
```

### Code Quality

```bash
# Lint code
flake8 speedtest/

# Sort imports
isort speedtest/

# Format code (if using black)
black speedtest/

# Run all pre-commit hooks
pre-commit run --all-files
```

## Project Structure

```
speedtest/
├── speedtest/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point
│   ├── config.py            # Configuration and logging
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── schemas.py       # JSON schema handling
│   │   ├── speedtest.py     # Core validation logic
│   │   └── templates.py     # Template rendering
│   ├── schemas/
│   │   └── schemaV1.json    # Default JSON schema
│   ├── templates/
│   │   ├── json.tpl         # JSON output template
│   │   └── influx.tpl       # InfluxDB template
│   └── tests/
│       ├── conftest.py      # Test configuration
│       ├── test_schema.py   # Schema validation tests
│       └── test_speedtest.py # Core logic tests
├── docs/                    # Documentation
├── setup.py                 # Package configuration
├── requirements.txt         # Dependencies
├── .flake8                 # Linting configuration
├── .isort.cfg              # Import sorting configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── README.md               # Main documentation
```

## Contributing Guidelines

### Code Style

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black's default)
- **Import sorting**: Use isort with the configuration in `.isort.cfg`
- **Linting**: Use flake8 with the configuration in `.flake8`

### Type Hints

- Use type hints for all public functions
- Import types from `typing` module
- Use `Optional[T]` for nullable values
- Use `Dict[str, Any]` for JSON-like data

Example:
```python
from typing import Dict, Optional, Any

def process_data(data: Dict[str, Any]) -> Optional[str]:
    if not data:
        return None
    return str(data)
```

### Documentation

- All public functions must have docstrings
- Use Google-style docstrings
- Include type information in docstrings
- Provide usage examples for complex functions

Example:
```python
def validate_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate a JSON schema against the JSON Schema Draft 7 specification.

    Args:
        schema: The JSON schema to validate.

    Returns:
        True if the schema is valid, False otherwise.

    Example:
        >>> schema = {"type": "string"}
        >>> validate_schema(schema)
        True
    """
```

### Testing

- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Test both success and failure cases

Example:
```python
def test_validate_schema_with_valid_schema():
    """Test that validate_schema returns True for valid schemas."""
    schema = {"type": "string", "pattern": "^[a-z]+$"}
    assert validate_schema(schema) is True

def test_validate_schema_with_invalid_pattern():
    """Test that validate_schema returns False for invalid regex patterns."""
    schema = {"type": "string", "pattern": "("}
    assert validate_schema(schema) is False
```

### Logging

- Use the module-level logger: `logger = logging.getLogger(__name__)`
- Use appropriate log levels:
  - `DEBUG`: Detailed diagnostic information
  - `INFO`: General information about program execution
  - `WARNING`: Something unexpected happened
  - `ERROR`: Serious problem occurred
  - `CRITICAL`: Very serious error occurred

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors with appropriate context
- Don't suppress exceptions unless necessary

Example:
```python
try:
    schema = json.load(file)
except json.JSONDecodeError as e:
    logger.error(f'Invalid JSON in schema file: {e}')
    return None
except FileNotFoundError:
    logger.error(f'Schema file not found: {schema_file}')
    return None
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps to trigger the bug
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: Python version, OS, speedtest CLI version
6. **Logs**: Relevant log output (use `--loglevel DEBUG`)

### Feature Requests

For new features, please provide:

1. **Use case**: Why this feature would be useful
2. **Description**: Detailed description of the proposed feature
3. **Implementation ideas**: If you have thoughts on implementation
4. **Backward compatibility**: How this affects existing functionality

### Code Contributions

#### Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your changes: `git checkout -b feature/my-new-feature`
3. **Write code** following the style guidelines
4. **Add tests** for your changes
5. **Update documentation** if needed
6. **Run tests** and linting: `pytest && flake8`
7. **Commit changes** with descriptive messages
8. **Push** to your fork: `git push origin feature/my-new-feature`
9. **Create a Pull Request** with a clear description

#### Commit Messages

Use clear, descriptive commit messages:

```
Add support for custom output templates

- Implement template discovery mechanism
- Add validation for template files
- Update CLI to accept template parameter
- Add tests for template functionality
```

### Documentation Contributions

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples or use cases
- Improve API documentation
- Create tutorials or guides

### Template Contributions

New output templates are valuable contributions:

1. Create the template file in `speedtest/templates/`
2. Test the template with real data
3. Document the template in the template guide
4. Add any special requirements or use cases

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

1. Update version in `setup.py`
2. Update `CHANGELOG.md` (if exists)
3. Run full test suite
4. Tag the release: `git tag v1.0.0`
5. Push tags: `git push --tags`

## Getting Help

- **Documentation**: Check the README and docs/ directory
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Ask for help in your pull request

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Useful Commands

```bash
# Run specific test
pytest speedtest/tests/test_schema.py::test_validate_schema_valid -v

# Run tests with debug output
pytest speedtest/tests/ -v -s --log-cli-level=DEBUG

# Check test coverage
pytest --cov=speedtest --cov-report=term-missing

# Lint specific file
flake8 speedtest/lib/schemas.py

# Check import order
isort speedtest/ --check-only --diff

# Format imports
isort speedtest/

# Run pre-commit on specific file
pre-commit run --files speedtest/lib/schemas.py
```

## Common Development Tasks

### Adding a New Template

1. Create the template file: `speedtest/templates/myformat.tpl`
2. Test the template manually
3. Add documentation to `docs/template-guide.md`
4. Consider adding tests if complex logic is involved

### Adding a New Schema Field

1. Update the schema: `speedtest/schemas/schemaV1.json`
2. Update any affected templates
3. Add tests for the new field validation
4. Update documentation

### Adding a New CLI Option

1. Add the option to the `@click.option` decorators in `__main__.py`
2. Update the main function signature
3. Implement the functionality
4. Add tests for the new option
5. Update the README and help text

Thank you for contributing to the speedtest CLI data logger!