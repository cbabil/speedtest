# Template Development Guide

This guide explains how to create custom templates for the speedtest CLI data logger.

## Template Basics

Templates use the [Jinja2 templating engine](https://jinja.palletsprojects.com/). They receive the speedtest output data as a variable called `jsondata`.

## Available Data Structure

The `jsondata` variable contains the following structure:

```json
{
  "type": "result",
  "timestamp": "2023-12-07T10:30:00.123456Z",
  "ping": {
    "jitter": 1.234,
    "latency": 15.567
  },
  "download": {
    "bandwidth": 50000000,
    "bytes": 62500000,
    "elapsed": 10000
  },
  "upload": {
    "bandwidth": 10000000,
    "bytes": 12500000,
    "elapsed": 10000
  },
  "serverSelection": {
    "selectedServerId": 12345,
    "selectedLatency": 15.567,
    "servers": [
      {
        "latency": 15.567,
        "server": {
          "id": 12345,
          "host": "speedtest.example.com",
          "port": 8080,
          "name": "Example Provider",
          "location": "New York, NY",
          "country": "United States"
        }
      }
    ]
  },
  "isp": "Example ISP",
  "interface": {
    "internalIp": "192.168.1.100",
    "name": "eth0",
    "macAddr": "00:11:22:33:44:55",
    "isVpn": false,
    "externalIp": "203.0.113.1"
  },
  "server": {
    "id": 12345,
    "host": "speedtest.example.com",
    "port": 8080,
    "name": "Example Provider",
    "location": "New York, NY",
    "country": "United States",
    "ip": "192.168.1.1"
  },
  "result": {
    "id": "abc123def456",
    "url": "https://www.speedtest.net/result/abc123def456",
    "persisted": true
  },
  "packetLoss": 0.0  // Optional field
}
```

## Helper Functions

Templates have access to the following helper functions:

### Date/Time Parsing

```jinja2
{% set dt = parser.parse(jsondata.timestamp) %}
{{ dt.isoformat() }}
{{ dt.strftime('%Y-%m-%d %H:%M:%S') }}
```

### Mathematical Operations

```jinja2
{# Convert bandwidth from bits/sec to Mbps #}
{{ (jsondata.download.bandwidth / 125000) | round(2) }}

{# Convert timestamp to nanoseconds #}
{% set ns = dt.timestamp() * 1e9 | round(0, 'floor') %}
{{ ns }}
```

## Template Examples

### CSV Template

Create `speedtest/templates/csv.tpl`:

```jinja2
{%- if not loop is defined -%}
timestamp,ping_latency,ping_jitter,download_mbps,upload_mbps,server_name,server_location,isp
{%- endif -%}
{{ jsondata.timestamp }},{{ jsondata.ping.latency }},{{ jsondata.ping.jitter }},{{ (jsondata.download.bandwidth / 125000) | round(2) }},{{ (jsondata.upload.bandwidth / 125000) | round(2) }},"{{ jsondata.server.name }}","{{ jsondata.server.location }}","{{ jsondata.isp }}"
```

### Prometheus Metrics Template

Create `speedtest/templates/prometheus.tpl`:

```jinja2
# HELP speedtest_ping_latency_seconds Ping latency in seconds
# TYPE speedtest_ping_latency_seconds gauge
speedtest_ping_latency_seconds{server_id="{{ jsondata.server.id }}",server_name="{{ jsondata.server.name }}",isp="{{ jsondata.isp }}"} {{ jsondata.ping.latency / 1000 }}

# HELP speedtest_ping_jitter_seconds Ping jitter in seconds
# TYPE speedtest_ping_jitter_seconds gauge
speedtest_ping_jitter_seconds{server_id="{{ jsondata.server.id }}",server_name="{{ jsondata.server.name }}",isp="{{ jsondata.isp }}"} {{ jsondata.ping.jitter / 1000 }}

# HELP speedtest_download_bits_per_second Download bandwidth in bits per second
# TYPE speedtest_download_bits_per_second gauge
speedtest_download_bits_per_second{server_id="{{ jsondata.server.id }}",server_name="{{ jsondata.server.name }}",isp="{{ jsondata.isp }}"} {{ jsondata.download.bandwidth }}

# HELP speedtest_upload_bits_per_second Upload bandwidth in bits per second
# TYPE speedtest_upload_bits_per_second gauge
speedtest_upload_bits_per_second{server_id="{{ jsondata.server.id }}",server_name="{{ jsondata.server.name }}",isp="{{ jsondata.isp }}"} {{ jsondata.upload.bandwidth }}

{%- if jsondata.packetLoss is defined %}
# HELP speedtest_packet_loss_percent Packet loss percentage
# TYPE speedtest_packet_loss_percent gauge
speedtest_packet_loss_percent{server_id="{{ jsondata.server.id }}",server_name="{{ jsondata.server.name }}",isp="{{ jsondata.isp }}"} {{ jsondata.packetLoss }}
{%- endif %}
```

### XML Template

Create `speedtest/templates/xml.tpl`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<speedtest>
  <timestamp>{{ jsondata.timestamp }}</timestamp>
  <server>
    <id>{{ jsondata.server.id }}</id>
    <name>{{ jsondata.server.name }}</name>
    <location>{{ jsondata.server.location }}</location>
    <country>{{ jsondata.server.country }}</country>
  </server>
  <client>
    <ip>{{ jsondata.interface.externalIp }}</ip>
    <isp>{{ jsondata.isp }}</isp>
  </client>
  <ping>
    <latency>{{ jsondata.ping.latency }}</latency>
    <jitter>{{ jsondata.ping.jitter }}</jitter>
  </ping>
  <download>
    <bandwidth_bps>{{ jsondata.download.bandwidth }}</bandwidth_bps>
    <bandwidth_mbps>{{ (jsondata.download.bandwidth / 125000) | round(2) }}</bandwidth_mbps>
    <bytes>{{ jsondata.download.bytes }}</bytes>
  </download>
  <upload>
    <bandwidth_bps>{{ jsondata.upload.bandwidth }}</bandwidth_bps>
    <bandwidth_mbps>{{ (jsondata.upload.bandwidth / 125000) | round(2) }}</bandwidth_mbps>
    <bytes>{{ jsondata.upload.bytes }}</bytes>
  </upload>
  {% if jsondata.packetLoss is defined -%}
  <packet_loss>{{ jsondata.packetLoss }}</packet_loss>
  {%- endif %}
</speedtest>
```

## Advanced Features

### Conditional Output

```jinja2
{%- if jsondata.packetLoss is defined and jsondata.packetLoss > 0 %}
Warning: Packet loss detected: {{ jsondata.packetLoss }}%
{%- endif %}
```

### String Escaping for Special Formats

For formats like InfluxDB that require special character escaping:

```jinja2
{# Escape spaces, commas, and quotes for InfluxDB #}
{{ jsondata.server.name | replace(' ', '\ ') | replace(',', '\,') | replace('"', '\\"') }}
```

### Looping Through Server Selection Data

```jinja2
{%- for server in jsondata.serverSelection.servers %}
Server {{ server.server.id }}: {{ server.server.name }} ({{ server.latency }}ms)
{%- endfor %}
```

## Template Validation

Templates are automatically validated when the application starts. Common validation errors include:

1. **Syntax Errors**: Check your Jinja2 syntax
2. **Missing Template**: Ensure the file exists in `speedtest/templates/`
3. **File Extension**: Template files must end with `.tpl`

## Testing Templates

To test your template without running a full speedtest:

1. Create a sample JSON file with speedtest data
2. Use a simple Python script to render the template:

```python
from speedtest.lib.templates import render_template
import json

with open('sample_data.json', 'r') as f:
    data = json.load(f)

result = render_template('speedtest/templates/your_template.tpl', data)
print(result)
```

## Best Practices

1. **Handle Missing Data**: Use the `default()` filter for optional fields
2. **Format Numbers**: Round floating-point numbers appropriately
3. **Escape Special Characters**: For formats that require it
4. **Add Comments**: Document complex template logic
5. **Test Edge Cases**: Consider empty or missing data scenarios

## Troubleshooting

### Common Issues

**Template not found:**
- Check file path and extension (.tpl)
- Verify the template is in the correct directory

**Rendering errors:**
- Check for undefined variables
- Use `default()` filters for optional data
- Validate Jinja2 syntax

**Output formatting issues:**
- Check string escaping for special characters
- Verify number formatting and precision