{{
    config(
        materialized='incremental',
        unique_key='dt',
        on_schema_change='sync_all_columns',
    )
}}

SELECT
    dt,
    user_id,
    first_name,
    last_name,
    country_code::VARCHAR(2) AS country_code,
    session_count,
    total_revenue
FROM {{ ref('agg_users_stage') }}
