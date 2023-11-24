{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- if node.name == var('tbl', '') -%}
        {{ logs('***NODE DEF2: ' ~ node ~ " ***") }}
        {{ 'something_dumb' }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}

{%- endmacro %}
