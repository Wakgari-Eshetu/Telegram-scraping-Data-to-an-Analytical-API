select
    m.message_id,
    c.channel_key,
    d.full_date as date_key,
    m.message_text,
    m.message_length,
    m.view_count,
    m.forward_count,
    m.has_image
FROM staging.stg_telegram_messages m
JOIN marts.dim_channels c
  ON m.channel_name = c.channel_name
JOIN marts.dim_dates d
  ON m.message_date = d.full_date;