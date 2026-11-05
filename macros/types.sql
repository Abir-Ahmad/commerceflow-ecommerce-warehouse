{% macro money_type() %}{% if target.type == 'bigquery' %}numeric{% else %}decimal(18,2){% endif %}{% endmacro %}
{% macro days_between(start, finish) %}
{% if target.type == 'bigquery' %}date_diff(cast({{ finish }} as date), cast({{ start }} as date), day)
{% else %}date_diff('day', cast({{ start }} as date), cast({{ finish }} as date)){% endif %}
{% endmacro %}
{% macro month_start(col) %}
{% if target.type == 'bigquery' %}date_trunc(cast({{ col }} as date), month)
{% else %}cast(date_trunc('month', {{ col }}) as date){% endif %}
{% endmacro %}
