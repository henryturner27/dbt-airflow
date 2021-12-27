
      

  create  table "dbt"."dev_hturner_core"."agg_users"
  as (
    

SELECT
    *
FROM "dbt"."dev_hturner_core_stage"."agg_users_stage"
  );
  