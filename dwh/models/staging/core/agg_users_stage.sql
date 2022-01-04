{{
    config(
        materialized='table',
        alias='agg_users_stage_' + var('ds_no_dash')
    )
}}

SELECT
    '{{ var('ds') }}' AS dt
  , a.user_id
  , a.first_name
  , a.last_name
  , a.country_code
  , COUNT(b.*) AS session_count
  , SUM(c.price) AS total_revenue
FROM {{ ref('users') }} a
LEFT JOIN {{ ref('sessions') }} b
    ON a.user_id = b.user_id
    AND DATE_TRUNC('day', b.created_at) <= '{{ var('ds') }}'
LEFT JOIN {{ ref('payments') }} c
    ON a.user_id = c.user_id
    AND DATE_TRUNC('day', c.created_at) <= '{{ var('ds') }}'
WHERE DATE_TRUNC('day', a.created_at) <= '{{ var('ds') }}'
GROUP BY 1,2,3,4,5
