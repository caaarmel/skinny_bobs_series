select DISTINCT
e.tourney_name,
strftime("%w", e.date) as actual_day_week,
case 
    when cast(strftime("%w", e.date) as INT) = 0 then "Sunday"
    when cast(strftime("%w", e.date) as INT) = 1 then "Monday"
    when cast(strftime("%w", e.date) as INT) = 2 then "Tuesday"
    when cast(strftime("%w", e.date) as INT) = 3 then "Wednesday"
    when cast(strftime("%w", e.date) as INT) = 4 then "Thursday"
    when cast(strftime("%w", e.date) as INT) = 5 then "Friday"
    when cast(strftime("%w", e.date) as INT) = 6 then "Saturday"
    end as actual_day_text,
(CAST(STRFTIME('%d', e.date) AS INTEGER) - 1) / 7 + 1 AS week_position,
et.name as event_type_name,
case when et.name = "weekly" and strftime("%w", e.date)  = es.day_of_week then "this one"
-- case when et.name = "monthly" 
end as check_this,
es.*
from 
events e
LEFT OUTER JOIN event_types et on e .event_type_id = et.id
LEFT OUTER JOIN event_subtypes es on es.event_type_id = et.id
 

-- select * from events where tourney_name = "8 Ball Tournament"
-- select distinct tourney, is_weekly, is_monthly, is_major, is_series, is_league, is_handicap  from staging_results where tourney like "8%ball%"CREATE VIEW season_2025_standings AS
