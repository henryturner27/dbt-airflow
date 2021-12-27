select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select *
from "dbt"."dev"."agg_users"
where unique_key is null



      
    ) dbt_internal_test