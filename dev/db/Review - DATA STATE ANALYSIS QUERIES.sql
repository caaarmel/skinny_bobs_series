-- DATA STATE ANALYSIS QUERIES
-- Run these to understand current state before implementing point calculations

-- 1. Check events table structure and subtype assignments
SELECT 
    'Events with subtype assignments' as check_type,
    COUNT(*) as total_events,
    COUNT(event_subtype_id) as events_with_subtype,
    COUNT(*) - COUNT(event_subtype_id) as events_missing_subtype
FROM events;

-- 2. See sample events and their current assignments
SELECT 
    id,
    tourney_name,
    date,
    roster,
    event_type_id,
    event_subtype_id,
    strftime('%w', date) as day_of_week -- 0=Sunday, 1=Monday, etc.
FROM events 
ORDER BY date DESC 
LIMIT 10;

-- 3. Check what event types we have
SELECT 
    et.id,
    et.name,
    COUNT(e.id) as event_count
FROM event_types et
LEFT JOIN events e ON e.event_type_id = et.id
GROUP BY et.id, et.name
ORDER BY et.id;

-- 4. Check what event subtypes are available
SELECT 
    es.id,
    es.name,
    es.event_type_id,
    et.name as event_type_name,
    es.day_of_week,
    es.tier,
    COUNT(e.id) as assigned_events
FROM event_subtypes es
JOIN event_types et ON es.event_type_id = et.id
LEFT JOIN events e ON e.event_subtype_id = es.id
GROUP BY es.id, es.name, es.event_type_id, et.name, es.day_of_week, es.tier
ORDER BY es.event_type_id, es.id;

-- 5. Check current point values in staging_results
SELECT 
    'Current points in staging_results' as analysis,
    COUNT(*) as total_records,
    COUNT(points) as records_with_points,
    MIN(points) as min_points,
    MAX(points) as max_points,
    AVG(points) as avg_points,
    COUNT(CASE WHEN points IS NULL THEN 1 END) as null_points
FROM staging_results;

-- 6. Sample of current points by position
SELECT 
    position_std,
    COUNT(*) as count,
    MIN(points) as min_points,
    MAX(points) as max_points,
    AVG(points) as avg_points
FROM staging_results 
WHERE points IS NOT NULL
GROUP BY position_std
ORDER BY position_std
LIMIT 10;

-- 7. Check if we have point_structures data
SELECT 
    'Point structures count' as check_type,
    COUNT(*) as total_structures
FROM point_structures;

-- 8. Sample of point structures we just created
SELECT 
    ps.event_subtype_id,
    es.name as subtype_name,
    ps.min_position,
    ps.max_position,
    ps.min_players,
    ps.max_players,
    ps.points_awarded
FROM point_structures ps
JOIN event_subtypes es ON ps.event_subtype_id = es.id
WHERE ps.min_position = 1  -- Just winners to see the structure
ORDER BY ps.event_subtype_id, ps.min_players;

-- 9. Check results view current state
SELECT 
    'Results view sample' as analysis,
    COUNT(*) as total_results
FROM results;

-- 10. Tournament name patterns (to help with subtype mapping)
SELECT 
    tourney_name,
    strftime('%w', date) as day_of_week,
    COUNT(*) as event_count,
    MIN(date) as first_date,
    MAX(date) as last_date
FROM events
GROUP BY tourney_name, strftime('%w', date)
ORDER BY event_count DESC, tourney_name;