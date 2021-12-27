

  create  table "dbt"."dev"."my_first_dbt_model__dbt_tmp"
  as (
    

SELECT
    *
FROM "dbt"."dev_dev"."users"
WHERE user_id BETWEEN 1 AND 3
  );