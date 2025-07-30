{%- macro format_timestamp(datetime) -%}
    {% set dt = parser.parse(datetime) %}
    "{{ dt.isoformat() }}"
{%- endmacro -%}

{
  "timestamp": {{ format_timestamp(jsondata.timestamp) }},
  "type": "{{ jsondata.type }}",
  "ping": {
    "jitter": {{ jsondata.ping.jitter | default('null') }},
    "latency": {{ jsondata.ping.latency | default('null') }}
  },
  "download": {
    "bandwidth_bits": {{ jsondata.download.bandwidth | default('null') }},
    "bandwidth_mbps": {{ (jsondata.download.bandwidth / 125000) | round(2) | default('null') }},
    "bytes": {{ jsondata.download.bytes | default('null') }},
    "elapsed": {{ jsondata.download.elapsed | default('null') }}
  },
  "upload": {
    "bandwidth_bits": {{ jsondata.upload.bandwidth | default('null') }},
    "bandwidth_mbps": {{ (jsondata.upload.bandwidth / 125000) | round(2) | default('null') }},
    "bytes": {{ jsondata.upload.bytes | default('null') }},
    "elapsed": {{ jsondata.upload.elapsed | default('null') }}
  },
  "server": {
    "id": {{ jsondata.server.id | default('null') }},
    "name": "{{ jsondata.server.name | default('Unknown') }}",
    "location": "{{ jsondata.server.location | default('Unknown') }}",
    "country": "{{ jsondata.server.country | default('Unknown') }}",
    "host": "{{ jsondata.server.host | default('Unknown') }}",
    "port": {{ jsondata.server.port | default('null') }},
    "ip": "{{ jsondata.server.ip | default('Unknown') }}"
  },
  "client": {
    "ip": "{{ jsondata.interface.externalIp | default('Unknown') }}",
    "lat": {{ jsondata.interface.lat | default('null') }},
    "lon": {{ jsondata.interface.lon | default('null') }},
    "isp": "{{ jsondata.isp | default('Unknown') }}",
    "country": "{{ jsondata.interface.country | default('Unknown') }}"
  },
  "result": {
    "id": "{{ jsondata.result.id | default('Unknown') }}",
    "url": "{{ jsondata.result.url | default('Unknown') }}",
    "persisted": {{ jsondata.result.persisted | default('false') | lower }}
  }{% if jsondata.packetLoss is defined %},
  "packetLoss": {{ jsondata.packetLoss }}{% endif %}
}