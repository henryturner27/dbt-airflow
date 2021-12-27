
      
    delete from "dbt"."dev"."agg_users"
    where (dt) in (
        select (dt)
        from "agg_users__dbt_tmp050727171621"
    );
    

    insert into "dbt"."dev"."agg_users" ("dt", "user_id", "first_name", "last_name", "country_code", "session_count", "total_revenue")
    (
        select "dt", "user_id", "first_name", "last_name", "country_code", "session_count", "total_revenue"
        from "agg_users__dbt_tmp050727171621"
    )
  