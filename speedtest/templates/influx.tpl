{###########################################}
{# Reusable Server Tags                    #}
{###########################################}
{% macro tags(path) -%}
speedtest_id={{ jsondata.result.id }},server_id={{ path.server.id }},server_name="{{ path.server.name | replace(' ', '\ ') | replace(',', '\,') | replace('"', '\\"') }}",server_location="{{ path.server.location | replace(' ', '\ ') | replace(',', '\,') | replace('"', '\\"') }}",server_country="{{ path.server.country | replace(' ', '\ ') | replace(',', '\,') | replace('"', '\\"') }}",isp="{{ jsondata.isp | replace(' ', '\ ') | replace(',', '\,') | replace('"', '\\"') }}"
{%- endmacro -%}

{##########################}
{# Reusable Timestamp     #}
{##########################}
{% macro timestampns(datetime) %}
    {% set dt = parser.parse(datetime) %}
    {% set ns = dt.timestamp() * 1e9 | round(0, 'floor') %}
    {{ ns }}
{% endmacro -%}

{###########################}
{# Reusable Measurement    #}
{###########################}
{% macro measurement(measurement_type, jsondatapath, measurement_keyword, measurement_data) %}
{%- if measurement_data is string %}
{{ measurement_type + ',' ~ tags(jsondatapath) + ' ' ~ measurement_keyword + '="' ~ measurement_data ~ '"' ~ ' ' ~ timestampns(jsondata.timestamp) | int }}
{%- else %}
{{ measurement_type + ',' ~ tags(jsondatapath) + ' ' ~ measurement_keyword + '=' ~ measurement_data ~ ' ' ~ timestampns(jsondata.timestamp) | int }}
{%- endif %}
{% endmacro -%}

{#- All Server Selection from speedtest json data #}
{% for servers in jsondata.serverSelection.servers %}
{{ measurement('serverSelection', servers, 'HostName', servers.server.host|string) }}
{{ measurement('serverSelection', servers, 'Latency', servers.latency) }}
{% endfor %}
{% if jsondata.ping %}
{{ measurement('ping', jsondata, 'jitter', jsondata.ping.jitter) }}
{{ measurement('ping', jsondata, 'latency', jsondata.ping.latency) }}
{% endif %}
{% if jsondata.download %}
{{ measurement('download', jsondata, 'bandwidth_bits', jsondata.download.bandwidth) }}
{{ measurement('download', jsondata, 'bandwidth_mbps', jsondata.download.bandwidth/125000) }}
{{ measurement('download', jsondata, 'bandwidth_bytes', jsondata.download.bytes) }}
{{ measurement('download', jsondata, 'bandwidth_elapsed', jsondata.download.elapsed) }}
{% endif %}
{% if jsondata.upload %}
{{ measurement('upload', jsondata, 'bandwidth_bits', jsondata.upload.bandwidth) }}
{{ measurement('upload', jsondata, 'bandwidth_mbps', jsondata.upload.bandwidth/125000) }}
{{ measurement('upload', jsondata, 'bandwidth_bytes', jsondata.upload.bytes) }}
{{ measurement('upload', jsondata, 'bandwidth_elapsed', jsondata.upload.elapsed) }}
{% endif %}
{% if jsondata.packetLoss is defined %}
{{ measurement('packetLoss', jsondata, 'packetLoss', jsondata.packetLoss) }}
{% endif %}
