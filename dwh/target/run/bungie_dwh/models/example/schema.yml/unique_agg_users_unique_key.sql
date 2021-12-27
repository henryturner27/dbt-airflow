select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    unique_key as unique_field,
    count(*) as n_records

from "dbt"."dev"."agg_users"
where unique_key is not null
group by unique_key
having count(*) > 1



      
    ) dbt_internal_test