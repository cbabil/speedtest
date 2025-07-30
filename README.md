# Speedtest CLI Data Logger

A comprehensive Python wrapper for the [Ookla Speedtest CLI](https://www.speedtest.net/apps/cli) that provides JSON schema validation, templating support, and structured output for network monitoring and analysis.

## Features

- **Speedtest CLI Integration**: Seamlessly wraps the official Ookla Speedtest CLI
- **JSON Schema Validation**: Validates speedtest output against configurable JSON schemas
- **Template Support**: Flexible Jinja2 templating for custom output formats
- **Multiple Output Formats**: Built-in support for JSON and InfluxDB line protocol
- **Robust Error Handling**: Comprehensive validation and error reporting
- **Configurable Logging**: Adjustable log levels for debugging and monitoring

## Prerequisites

1. **Ookla Speedtest CLI**: This tool requires the official Ookla Speedtest CLI to be installed and available in your system PATH.

   - **Download**: Visit [https://www.speedtest.net/apps/cli](https://www.speedtest.net/apps/cli)
   - **Install**: Follow the installation instructions for your operating system
   - **Verify**: Run `speedtest --version` to confirm installation

2. **Python**: Requires Python 3.8 or higher

## Installation

### From Source

```bash
git clone https://github.com/cbabil/speedtest.git
cd speedtest
pip install -e .
```

### Using pip (if published)

```bash
pip install speedtest
```

## Usage

### Basic Usage

Run a speedtest and output results in JSON format:

```bash
python -m speedtest
```

### Command Line Options

```bash
python -m speedtest [OPTIONS]

Options:
  --template TEXT  Template to be used [default: json]
  --schema TEXT    Speedtest schema [default: speedtest/schemas/schemaV1.json]
  --out TEXT       Output for the data [default: stdout]
  --loglevel TEXT  Log Level [default: INFO]
  --help           Show this message and exit.
```

### Examples

**Output to a file:**
```bash
python -m speedtest --out speedtest_results.json
```

**Use InfluxDB template for time-series databases:**
```bash
python -m speedtest --template influx --out speedtest.influx
```

**Custom schema validation:**
```bash
python -m speedtest --schema custom_schema.json
```

**Debug mode:**
```bash
python -m speedtest --loglevel DEBUG
```

## Output Formats

### JSON Template (Default)

The default JSON template provides a clean, structured output:

```json
{
  "timestamp": "2023-12-07T10:30:00Z",
  "type": "result",
  "ping": {
    "jitter": 1.2,
    "latency": 15.5
  },
  "download": {
    "bandwidth_bits": 50000000,
    "bandwidth_mbps": 400.0,
    "bytes": 62500000,
    "elapsed": 10000
  },
  "upload": {
    "bandwidth_bits": 10000000,
    "bandwidth_mbps": 80.0,
    "bytes": 12500000,
    "elapsed": 10000
  },
  "server": {
    "id": 12345,
    "name": "Example Provider",
    "location": "New York, NY",
    "country": "United States",
    "host": "speedtest.example.com",
    "port": 8080,
    "ip": "192.168.1.1"
  },
  "client": {
    "ip": "203.0.113.1",
    "isp": "Example ISP",
    "country": "United States"
  },
  "result": {
    "id": "abc123def456",
    "url": "https://www.speedtest.net/result/abc123def456",
    "persisted": true
  }
}
```

### InfluxDB Template

The InfluxDB template formats data for time-series databases:

```
serverSelection,speedtest_id=abc123,server_id=12345,server_name=Example\ Provider,server_location=New\ York\,\ NY,server_country=United\ States,isp=Example\ ISP HostName="speedtest.example.com" 1701944400000000000
ping,speedtest_id=abc123,server_id=12345,server_name=Example\ Provider,server_location=New\ York\,\ NY,server_country=United\ States,isp=Example\ ISP jitter=1.2 1701944400000000000
ping,speedtest_id=abc123,server_id=12345,server_name=Example\ Provider,server_location=New\ York\,\ NY,server_country=United\ States,isp=Example\ ISP latency=15.5 1701944400000000000
download,speedtest_id=abc123,server_id=12345,server_name=Example\ Provider,server_location=New\ York\,\ NY,server_country=United\ States,isp=Example\ ISP bandwidth_bits=50000000 1701944400000000000
download,speedtest_id=abc123,server_id=12345,server_name=Example\ Provider,server_location=New\ York\,\ NY,server_country=United\ States,isp=Example\ ISP bandwidth_mbps=400.0 1701944400000000000
```

## Schema Validation

The tool validates speedtest output against JSON schemas to ensure data integrity. The default schema (`speedtest/schemas/schemaV1.json`) defines the expected structure of speedtest results.

### Custom Schemas

You can provide custom schemas for specific validation requirements:

```bash
python -m speedtest --schema /path/to/custom/schema.json
```

### Schema Features

- **JSON Schema Draft 7** compliance
- **Regex pattern validation** for string fields
- **Type checking** for all data fields
- **Required field validation**
- **Error reporting** with detailed validation messages

## Custom Templates

Create custom output formats using Jinja2 templates. Templates should be placed in the `speedtest/templates/` directory with a `.tpl` extension.

### Template Variables

Templates have access to the `jsondata` variable containing the speedtest results:

- `jsondata.timestamp` - Test timestamp
- `jsondata.ping.jitter` - Ping jitter in ms
- `jsondata.ping.latency` - Ping latency in ms  
- `jsondata.download.bandwidth` - Download bandwidth in bits/sec
- `jsondata.upload.bandwidth` - Upload bandwidth in bits/sec
- `jsondata.server.*` - Server information
- `jsondata.isp` - ISP name
- And more...

### Template Functions

Templates also have access to helper functions:

- `parser.parse()` - Parse ISO datetime strings
- Jinja2 built-in filters and functions

### Example Custom Template

Create `speedtest/templates/csv.tpl`:

```jinja2
timestamp,ping_latency,ping_jitter,download_mbps,upload_mbps,server_name,isp
{{ jsondata.timestamp }},{{ jsondata.ping.latency }},{{ jsondata.ping.jitter }},{{ (jsondata.download.bandwidth / 125000) | round(2) }},{{ (jsondata.upload.bandwidth / 125000) | round(2) }},"{{ jsondata.server.name }}","{{ jsondata.isp }}"
```

Use with:
```bash
python -m speedtest --template csv --out results.csv
```

## Development

### Running Tests

```bash
pytest speedtest/tests/ -v
```

### Code Quality

The project uses several tools for code quality:

```bash
# Linting
flake8 speedtest/

# Import sorting
isort speedtest/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Project Structure

```
speedtest/
├── speedtest/
│   ├── __init__.py
│   ├── __main__.py          # Main CLI entry point
│   ├── config.py            # Logging configuration
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── schemas.py       # Schema validation
│   │   ├── speedtest.py     # Core speedtest logic
│   │   └── templates.py     # Template rendering
│   ├── schemas/
│   │   └── schemaV1.json    # Default JSON schema
│   ├── templates/
│   │   ├── json.tpl         # JSON output template
│   │   └── influx.tpl       # InfluxDB template
│   └── tests/
│       ├── conftest.py
│       ├── test_schema.py
│       └── test_speedtest.py
├── setup.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Troubleshooting

### Common Issues

**Speedtest CLI not found:**
```
ERROR - unable to find speedtest. Is it installed?
```
- Solution: Install the Ookla Speedtest CLI and ensure it's in your PATH

**Template not found:**
```
ERROR - Template "custom" not found in any of the expected locations
```
- Solution: Ensure your template file exists in `speedtest/templates/` with a `.tpl` extension

**Schema validation failed:**
```
ERROR - Schema validation error: Invalid regex pattern
```
- Solution: Check your schema file for invalid regex patterns in `pattern` fields

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
python -m speedtest --loglevel DEBUG
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Repository**: [https://github.com/cbabil/speedtest](https://github.com/cbabil/speedtest)
- **Issues**: [https://github.com/cbabil/speedtest/issues](https://github.com/cbabil/speedtest/issues)
- **Ookla Speedtest CLI**: [https://www.speedtest.net/apps/cli](https://www.speedtest.net/apps/cli)
