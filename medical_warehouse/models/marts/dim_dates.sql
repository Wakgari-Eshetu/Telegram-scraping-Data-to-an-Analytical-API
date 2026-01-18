with dates as (
    select distinct post_date
    from staging.stg_telegram_messages
)

select
    post_date as full_date,
    extract(doy from post_date)::int as day_of_year,
    extract(dow from post_date)::int as day_of_week,
    to_char(post_date,'Day') as day_name,
    extract(week from post_date)::int as week_of_year,
    extract(month from post_date)::int as month,
    to_char(post_date,'Month') as month_name,
    extract(quarter from post_date)::int as quarter,
    extract(year from post_date)::int as year,
    case 
        when extract(dow from post_date) in (0,6) 
        then true 
        else false 
    end as is_weekend
from dates;
