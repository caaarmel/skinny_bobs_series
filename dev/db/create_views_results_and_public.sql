-- RESULTS VIEWS WITH CALCULATED POINTS
-- These views calculate points on-the-fly from point_structures table
-- Replaces static points from imports with dynamic calculated points

-- DROP existing views first
DROP VIEW IF EXISTS results;
DROP VIEW IF EXISTS results_public;
DROP VIEW IF EXISTS season_2025_standings;

-- MAIN RESULTS VIEW with calculated points
CREATE VIEW results AS
SELECT
  sr.id AS id,
  p.id AS player_id,
  e.id AS event_id,
  sr.prize AS prize,
  
  -- CALCULATED POINTS: Look up from point_structures table
  -- Use subquery to find the BEST matching point structure (highest min_players that qualifies)
  COALESCE((
    SELECT ps.points_awarded
    FROM point_structures ps
    WHERE ps.event_subtype_id = e.event_subtype_id
      AND sr.position_std >= ps.min_position 
      AND (ps.max_position IS NULL OR sr.position_std <= ps.max_position)
      AND e.roster >= ps.min_players
      AND (ps.max_players IS NULL OR e.roster <= ps.max_players)
      AND ps.season_id_start <= e.season_id
      AND (ps.season_id_end IS NULL OR ps.season_id_end >= e.season_id)
      AND ps.is_active = 1
    ORDER BY ps.min_players DESC  -- Get the most specific bracket (highest min_players)
    LIMIT 1
  ), 0) AS points,
  
  sr.position AS position_orig,
  sr.position_std AS position_std,
  sr.id AS source_id,
  sr.processed_datetime AS created_at,
  NULL AS updated_at,
  
  -- Additional useful fields for analysis
  e.roster AS event_roster,
  e.event_subtype_id AS event_subtype_id,
  es.name AS event_subtype_name,
  es.tier AS event_subtype_tier,
  et.name AS event_type_name

FROM staging_results sr
JOIN players p ON p.full_name = sr.full_name
JOIN events e ON e.tourney_slug = sr.tourney AND e.date = sr.date
LEFT JOIN event_subtypes es ON e.event_subtype_id = es.id
LEFT JOIN event_types et ON e.event_type_id = et.id;

-- PUBLIC RESULTS VIEW for external display
CREATE VIEW results_public AS
SELECT
  p.full_name AS "Player",
  e.tourney_name AS "Tournament", 
  strftime('%Y-%m-%d', e.date) AS "Date",
  CASE WHEN r.position_std = 1 THEN "1st"
       ELSE r.position_orig 
       END AS "Place Original",
  r.position_std AS "Place",
  r.points AS "Points",  -- Now using calculated points
  r.prize AS "Prize",
  r.event_type_name AS "Event Type",
  r.event_subtype_name AS "Event Subtype",
  r.event_subtype_tier AS "Tier",
  e.roster AS "Players"
FROM results r
JOIN players p ON r.player_id = p.id  
JOIN events e ON r.event_id = e.id
ORDER BY e.date DESC;

-- SEASON STANDINGS VIEW (Core Leaderboard) with calculated points
CREATE VIEW season_2025_standings AS
SELECT
  p.full_name AS "Player",
  
  -- Core Statistics
  SUM(r.points) AS "Total Points",  -- Main ranking criteria
  COUNT(r.id) AS "Total Events",
  COUNT(CASE WHEN r.position_std = 1 THEN 1 END) AS "Wins",
  COUNT(CASE WHEN r.position_std <= 3 THEN 1 END) AS "Top 3",
  COUNT(CASE WHEN r.position_std <= 8 THEN 1 END) AS "Top 8",
  
  -- Performance Metrics (as percentages)
  ROUND(
    (COUNT(CASE WHEN r.position_std = 1 THEN 1 END) * 100.0) / COUNT(r.id), 
    1
  ) AS "Win Rate %",
  ROUND(
    (COUNT(CASE WHEN r.position_std <= 3 THEN 1 END) * 100.0) / COUNT(r.id), 
    1
  ) AS "Top 3 Rate %",
  
  -- Activity
  date(MAX(e.date)) AS "Last Played"

FROM results r
JOIN players p ON r.player_id = p.id
JOIN events e ON r.event_id = e.id

WHERE e.season_id = 1

GROUP BY p.full_name
ORDER BY SUM(r.points) DESC NULLS LAST, 
         COUNT(CASE WHEN r.position_std = 1 THEN 1 END) DESC, 
         COUNT(CASE WHEN r.position_std <= 3 THEN 1 END) DESC;

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