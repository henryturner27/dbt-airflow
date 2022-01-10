{{
    config(
        materialized='incremental',
        unique_key='dt',
        on_schema_change='sync_all_columns',
    )
}}

SELECT
    *
FROM {{ ref('agg_users_stage') }}
