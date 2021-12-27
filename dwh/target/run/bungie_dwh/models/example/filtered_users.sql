

  create  table "dbt"."dev"."filtered_users__dbt_tmp"
  as (
    

SELECT
    *
FROM "dbt"."dev_dev"."users"
WHERE user_id BETWEEN 1 AND 3
  );