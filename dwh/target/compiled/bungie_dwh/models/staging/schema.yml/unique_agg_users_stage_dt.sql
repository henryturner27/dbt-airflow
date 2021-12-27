
    
    

select
    dt as unique_field,
    count(*) as n_records

from "dbt"."dev"."agg_users_stage"
where dt is not null
group by dt
having count(*) > 1


