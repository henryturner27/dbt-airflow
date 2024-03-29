{{
    config(
        materialized='table',
        schema='core_stage',
        alias='agg_users_stage_' + var('ds_nodash'),
    )
}}

SELECT
    '{{ var('ds') }}'::DATE AS dt,
    a.user_id,
    a.first_name,
    a.last_name,
    a.country_code,
    COUNT(b.*) AS session_count,
    COALESCE(SUM(c.price), 0) AS total_revenue
--   , CONCAT(a.first_name, ' ', a.last_name) AS first_last
FROM {{ ref('users') }} AS a
LEFT JOIN {{ ref('sessions') }} AS b
    ON a.user_id = b.user_id
    AND DATE_TRUNC('day', b.created_at) <= '{{ var('ds') }}'
LEFT JOIN {{ ref('payments') }} AS c
    ON a.user_id = c.user_id
    AND DATE_TRUNC('day', c.created_at) <= '{{ var('ds') }}'
WHERE DATE_TRUNC('day', a.created_at) <= '{{ var('ds') }}'
GROUP BY 1, 2, 3, 4, 5
