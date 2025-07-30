# Speedtest Logger

## Description

This Python script runs a speedtest using the official `speedtest` CLI tool, validates the JSON output against a schema, and then formats the data using a template. The output can be directed to either a file or to standard output.

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/your-username/speedtest-logger.git
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    *   **Windows:**
        ```bash
        venv\\Scripts\\activate
        ```
    *   **macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  Install the project in editable mode:
    ```bash
    pip install -e .
    ```
5.  Install the `speedtest` CLI tool. You can find instructions on the official Speedtest website: [https://www.speedtest.net/apps/cli](https://www.speedtest.net/apps/cli)

## Usage

```bash
speedtest-logger --help
```

### Options

*   `--template`: The template to use for formatting the output. Defaults to `json`.
*   `--schema`: The JSON schema to use for validating the speedtest output. Defaults to `speedtest/schemas/schemaV1.json`.
*   `--out`: The destination for the output. Defaults to `stdout`.
*   `--loglevel`: The logging level. Defaults to `INFO`.

### Examples

*   Run a speedtest and print the JSON output to the console:
    ```bash
    speedtest-logger
    ```
*   Run a speedtest and save the output to a file named `speedtest.log`:
    ```bash
    speedtest-logger --out speedtest.log
    ```
*   Run a speedtest and format the output using the `influx` template:
    ```bash
    speedtest-logger --template influx
    ```
