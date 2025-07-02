--CREATE VIEW IF NOT EXISTS view_event_structures AS
SELECT DISTINCT 
e.name as event_type
, et.name as event_subtype
, et.tier
,case 
    when et.day_of_week = 0 then "Sunday"
    when et.day_of_week = 1 then "Monday"
    when et.day_of_week = 2 then "Tuesday"
    when et.day_of_week = 3 then "Wednesday"
    when et.day_of_week = 4 then "Thursday"
    when et.day_of_week = 5 then "Friday"
    when et.day_of_week = 6 then "Saturday"
    end as day_of_week
--, ps.*
FROM
event_types e
LEFT OUTER JOIN event_subtypes et ON et.event_type_id = e.id
LEFT OUTER JOIN point_structures ps on ps.event_subtype_id = et.id