select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select *
from "dbt"."dev"."agg_users_stage"
where user_id is null



      
    ) dbt_internal_test