{% test length(model, column_name, len_val) %}
    select * from {{ model }} where length({{ column_name }}) <> {{ len_val }}
{% endtest %}
