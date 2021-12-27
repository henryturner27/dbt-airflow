

  create  table "dbt"."dev"."agg_users_stage__dbt_tmp"
  as (
    

SELECT
    '2021-12-26' AS dt
  , a.user_id
  , a.first_name
  , a.last_name
  , a.country_code
  , COUNT(b.*) AS session_count
  , SUM(c.price) AS total_revenue
FROM "dbt"."dev"."users" a
LEFT JOIN "dbt"."dev"."sessions" b
    ON a.user_id = b.user_id
    AND DATE_TRUNC('day', b.created_at) <= '2021-12-26'
LEFT JOIN "dbt"."dev"."payments" c
    ON a.user_id = c.user_id
    AND DATE_TRUNC('day', c.created_at) <= '2021-12-26'
WHERE DATE_TRUNC('day', a.created_at) <= '2021-12-26'
GROUP BY 1,2,3,4,5
  );