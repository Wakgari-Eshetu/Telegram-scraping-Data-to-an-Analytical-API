with raw as (
    select *
    from raw.telegram_messages
)

select
    message_id,
    channel_name,
    message_text,
    view_count::int as view_count,
    forward_count::int as forward_count,
    date::date as post_date,
    char_length(message_text) as message_length,
    case when image_path is not null then true else false end as has_image
from raw
where message_text is not null
