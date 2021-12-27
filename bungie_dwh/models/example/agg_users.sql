{{
    config(
        materialized='incremental',
        unique_key='dt'
    )
}}

SELECT
    *
FROM {{ ref('agg_users_stage') }}
