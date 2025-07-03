-- RESULTS VIEWS WITH CALCULATED POINTS
-- These views calculate points on-the-fly from point_structures table
-- Replaces static points from imports with dynamic calculated points

-- DROP existing views first
DROP VIEW IF EXISTS results_public;
DROP VIEW IF EXISTS season_standings;
DROP VIEW IF EXISTS season_2025_standings;


-- PUBLIC RESULTS VIEW for external display
CREATE VIEW iF NOT EXISTS results_public AS
select distinct
s.name as season,
e.tourney_name as tournament,
e.date,
e.roster as total_players,
es.name as event_subtype,
ps.name as pt_structure,
p.full_name,
case when r.position_std = 1 then "1st"
    else r.position
    end as position_orig,
r.position_std,
ifnull(ps.points_awarded,0) as points,
et.name as event_type_name,

p.first_name,
p.last_name,
p.alias,

e.id as event_id,
e.event_type_id,
e.event_subtype_id,
ps.id as ps_id,
ps.min_position as ps_min_pos,
ps.max_position as ps_max_pos,
r.source_id,
r.created_at,
r.processed_datetime

from staging_results r 
left outer join players p on r.full_name = p.full_name
left outer join events e on r.tourney = e.tourney_slug and r.date = e.date
left outer join seasons s on e.season_id = s.id
left outer join event_types et on e.event_type_id = et.id
left outer join event_subtypes es on e.event_subtype_id = es.id
left outer join point_structures ps
    on e.event_subtype_id = ps.event_subtype_id
    and (e.season_id between ps.season_id_start and ifnull(ps.season_id_end,99))
    and (e.roster between ps.min_players and ifnull(ps.max_players,999) )
    and (r.position_std between ps.min_position and ifnull(ps.max_position,999))
    and (r.position_std between ps.min_position and ifnull(ps.max_players,999))
order by s.name desc, e.date, r.position_std, p.first_name
;

-- SEASON STANDINGS VIEW (Core Leaderboard) with calculated points
CREATE VIEW season_standings AS
SELECT
    rp.season,
    rp.full_name AS player,

    -- Core Statistics
    SUM(rp.points) AS total_pts,  -- Main ranking criteria
    COUNT(rp.event_id) AS total_events,
    COUNT(CASE WHEN rp.position_std = 1 THEN 1 END) AS wins,
    COUNT(CASE WHEN rp.position_std <= 3 THEN 1 END) AS top_3,
    COUNT(CASE WHEN rp.position_std <= 8 THEN 1 END) AS top_8,

    -- Event Type Breakdown (excluding series and league)
    COUNT(CASE WHEN rp.event_type_name = 'weekly' THEN 1 END) AS weekly_events,
    COUNT(CASE WHEN rp.event_type_name = 'monthly' THEN 1 END) AS monthly_events, 
    COUNT(CASE WHEN rp.event_type_name = 'major' THEN 1 END) AS major_events,

    -- Performance Metrics (as percentages)
    ROUND(
    (COUNT(CASE WHEN rp.position_std = 1 THEN 1 END) * 100.0) / COUNT(rp.event_id), 
    1
    ) AS win_rate_pct,
    ROUND(
    (COUNT(CASE WHEN rp.position_std <= 3 THEN 1 END) * 100.0) / COUNT(rp.event_id), 
    1
    ) AS top_3_pct,

    -- Activity
    date(MAX(rp.date)) AS last_played

FROM results_public rp

-- Filter out series and league events
WHERE rp.event_id IS NOT NULL  -- Ensure valid events
  AND rp.event_type_name NOT IN ('series', 'league')

GROUP BY rp.full_name, rp.season
ORDER BY rp.season desc,
    SUM(rp.points) DESC NULLS LAST, 
    COUNT(CASE WHEN rp.position_std = 1 THEN 1 END) DESC, 
    COUNT(CASE WHEN rp.position_std <= 3 THEN 1 END) DESC;


-- FAKE!!! ALL POINTS FROM 2024 and 2025
CREATE VIEW season_2025_standings AS
SELECT
    rp.full_name AS player,

    -- Core Statistics
    SUM(rp.points) AS total_pts,  -- Main ranking criteria
    COUNT(rp.event_id) AS total_events,
    COUNT(CASE WHEN rp.position_std = 1 THEN 1 END) AS wins,
    COUNT(CASE WHEN rp.position_std <= 3 THEN 1 END) AS top_3,
    COUNT(CASE WHEN rp.position_std <= 8 THEN 1 END) AS top_8,

    -- Event Type Breakdown (excluding series and league)
    COUNT(CASE WHEN rp.event_type_name = 'weekly' THEN 1 END) AS weekly_events,
    COUNT(CASE WHEN rp.event_type_name = 'monthly' THEN 1 END) AS monthly_events, 
    COUNT(CASE WHEN rp.event_type_name = 'major' THEN 1 END) AS major_events,

    -- Performance Metrics (as percentages)
    ROUND(
    (COUNT(CASE WHEN rp.position_std = 1 THEN 1 END) * 100.0) / COUNT(rp.event_id), 
    1
    ) AS win_rate_pct,
    ROUND(
    (COUNT(CASE WHEN rp.position_std <= 3 THEN 1 END) * 100.0) / COUNT(rp.event_id), 
    1
    ) AS top_3_pct,

    -- Activity
    date(MAX(rp.date)) AS last_played

FROM results_public rp

-- Filter out series and league events
WHERE rp.event_id IS NOT NULL  -- Ensure valid events
  AND rp.event_type_name NOT IN ('series', 'league')

GROUP BY rp.full_name
ORDER BY 
    SUM(rp.points) DESC NULLS LAST, 
    COUNT(CASE WHEN rp.position_std = 1 THEN 1 END) DESC, 
    COUNT(CASE WHEN rp.position_std <= 3 THEN 1 END) DESC;


-- VALIDATION QUERIES to test the point calculations

-- 1. Check that points are being calculated (not all zeros)
SELECT 
    'Points calculation check' as test,
    COUNT(*) as total_results,
    COUNT(CASE WHEN points > 0 THEN 1 END) as results_with_points,
    COUNT(CASE WHEN points = 0 THEN 1 END) as results_with_zero_points,
    ROUND(AVG(points), 2) as avg_points
FROM results;

-- 2. Sample results showing point calculation details
SELECT 
    player_id,
    event_subtype_name,
    event_subtype_tier,
    position_orig,
    position_std,
    event_roster,
    points,
    -- Show which point structure was matched
    'pos:' || position_std || ' roster:' || event_roster as lookup_key
FROM results 
WHERE points > 0
ORDER BY points DESC
LIMIT 10;

-- 3. Check for results that didn't get points (troubleshooting)
SELECT 
    event_subtype_name,
    event_subtype_tier,
    position_orig,
    position_std,
    event_roster,
    COUNT(*) as count_missing_points
FROM results 
WHERE points = 0 OR points IS NULL
GROUP BY event_subtype_name, event_subtype_tier, position_orig, position_std, event_roster
ORDER BY count_missing_points DESC
LIMIT 10;

-- 4. Diagnostic: Check point structure coverage for missing points
SELECT DISTINCT
    'Point structure coverage check' as analysis,
    sr.position_std,
    e.roster,
    e.event_subtype_id,
    es.name as event_subtype_name,
    ps.min_position,
    ps.max_position,
    ps.min_players,
    ps.max_players,
    ps.points_awarded
FROM staging_results sr
JOIN events e ON e.tourney_slug = sr.tourney AND e.date = sr.date  
JOIN event_subtypes es ON e.event_subtype_id = es.id
LEFT JOIN point_structures ps ON (
    ps.event_subtype_id = e.event_subtype_id
    AND sr.position_std >= ps.min_position 
    AND (ps.max_position IS NULL OR sr.position_std <= ps.max_position)
    AND e.roster >= ps.min_players
    AND (ps.max_players IS NULL OR e.roster <= ps.max_players)
    AND ps.is_active = 1
)
WHERE ps.points_awarded IS NULL
ORDER BY sr.position_std, e.roster
LIMIT 20;

-- 5. Debug: Check what event_subtype_id values exist in events
SELECT DISTINCT
    'Event subtypes in events table' as check_type,
    e.event_subtype_id,
    es.name as event_subtype_name,
    COUNT(e.id) as event_count
FROM events e
JOIN event_subtypes es ON e.event_subtype_id = es.id
GROUP BY e.event_subtype_id, es.name
ORDER BY e.event_subtype_id;

-- 6. Debug: Check what event_subtype_id values exist in point_structures  
SELECT DISTINCT
    'Event subtypes in point_structures' as check_type,
    ps.event_subtype_id,
    es.name as event_subtype_name,
    ps.season_id_start,
    ps.is_active,
    COUNT(ps.id) as structure_count
FROM point_structures ps
JOIN event_subtypes es ON ps.event_subtype_id = es.id
GROUP BY ps.event_subtype_id, es.name, ps.season_id_start, ps.is_active
ORDER BY ps.event_subtype_id;

-- 8. Debug: Test season logic specifically
SELECT 
    'Season logic test' as test,
    ps.season_id_start,
    ps.season_id_end,
    e.season_id as event_season,
    -- Test season conditions
    CASE WHEN ps.season_id_start <= e.season_id THEN 'PASS' ELSE 'FAIL' END as season_start_check,
    CASE WHEN (ps.season_id_end IS NULL OR ps.season_id_end >= e.season_id) THEN 'PASS' ELSE 'FAIL' END as season_end_check,
    COUNT(*) as combinations
FROM events e
CROSS JOIN point_structures ps
WHERE e.event_subtype_id = ps.event_subtype_id
GROUP BY ps.season_id_start, ps.season_id_end, e.season_id
ORDER BY e.season_id, ps.season_id_start
LIMIT 10;

-- 9. Debug: Simple point lookup test for one specific case
SELECT 
    'Simple lookup test' as test,
    e.event_subtype_id,
    es.name as subtype_name,
    e.season_id,
    e.roster,
    sr.position_std,
    ps.min_position,
    ps.max_position,
    ps.min_players,
    ps.max_players,
    ps.season_id_start,
    ps.season_id_end,
    ps.is_active,
    ps.points_awarded
FROM events e
JOIN staging_results sr ON e.tourney_slug = sr.tourney AND e.date = sr.date
JOIN event_subtypes es ON e.event_subtype_id = es.id
LEFT JOIN point_structures ps ON ps.event_subtype_id = e.event_subtype_id
WHERE sr.position_std = 1 AND e.roster = 17  -- Pick a specific case
LIMIT 5;

-- 5. Points by event subtype (should match your point structure ranges)
SELECT 
    event_subtype_name,
    event_subtype_tier,
    MIN(points) as min_points,
    MAX(points) as max_points,
    ROUND(AVG(points), 1) as avg_points,
    COUNT(*) as result_count
FROM results 
WHERE points > 0
GROUP BY event_subtype_name, event_subtype_tier
ORDER BY event_subtype_tier DESC, max_points DESC;