/*
delete from point_structures
where event_subtype_id in (1,2,3,4,5)
*/

-- Standard Point Structures for Generic Event Subtypes
-- These are fallback point values at 75% of the explicit tier values
-- For use when events don't have specific stakeholder-designed point structures
-- CORRECTED VERSION: Fixed point value ties to ensure proper progression
--
-- STANDARD POINT VALUES REFERENCE (Winner Points):
-- +------------------+--------------+--------------+--------------+
-- | Event Type       | 25-32 Player | 17-24 Player | 8-16 Players |
-- +------------------+--------------+--------------+--------------+
-- | Standard Major   |     120      |     110      |     100      |
-- | Standard Monthly |      80      |      75      |      70      |
-- | Standard Series  |      80      |      75      |      70      |
-- | Standard Weekly  |      40      |      35      |      30      |
-- | Standard League  |      35      |      30      |      25      |
-- +------------------+--------------+--------------+--------------+

-- STANDARD MAJOR (Tier 4 equivalent - 75% of 160 base, rounded to 5s)
-- event_subtype_id = 4 (from event_subtypes table)
INSERT INTO point_structures(name,season_id_start, event_subtype_id, min_position, max_position, min_players, max_players, points_awarded)
VALUES  
    -- 25-32 players
    ('std major 25-32 players',1,4,1,1,25,NULL,120),
    ('std major 25-32 players',1,4,2,2,25,NULL,95),
    ('std major 25-32 players',1,4,3,4,25,NULL,70),
    ('std major 25-32 players',1,4,5,8,25,NULL,55),
    ('std major 25-32 players',1,4,9,16,25,NULL,25),
    ('std major 25-32 players',1,4,17,24,25,NULL,20),
    ('std major 25-32 players',1,4,25,NULL,25,NULL,15),

    -- 17-24 players  
    ('std major 17-24 players',1,4,1,1,17,24,110),
    ('std major 17-24 players',1,4,2,2,17,24,85),
    ('std major 17-24 players',1,4,3,4,17,24,60),
    ('std major 17-24 players',1,4,5,8,17,24,45),
    ('std major 17-24 players',1,4,9,16,17,24,15),
    ('std major 17-24 players',1,4,17,24,17,24,10),

    -- 8-16 players
    ('std major 8-16 players',1,4,1,1,8,16,100),
    ('std major 8-16 players',1,4,2,2,8,16,75),
    ('std major 8-16 players',1,4,3,4,8,16,50),
    ('std major 8-16 players',1,4,5,8,8,16,35),
    ('std major 8-16 players',1,4,9,16,8,16,5),

-- STANDARD MONTHLY (Tier 3 equivalent - upgraded to 80 base, rounded to 5s)
-- event_subtype_id = 2 (from event_subtypes table)
    -- 25-32 players
    ('std monthly 25-32 players',1,2,1,1,25,NULL,80),
    ('std monthly 25-32 players',1,2,2,2,25,NULL,70),
    ('std monthly 25-32 players',1,2,3,3,25,NULL,70),
    ('std monthly 25-32 players',1,2,4,4,25,NULL,60),
    ('std monthly 25-32 players',1,2,5,6,25,NULL,55),
    ('std monthly 25-32 players',1,2,7,8,25,NULL,45),
    ('std monthly 25-32 players',1,2,9,12,25,NULL,45),
    ('std monthly 25-32 players',1,2,13,16,25,NULL,35),
    ('std monthly 25-32 players',1,2,17,24,25,NULL,25),
    ('std monthly 25-32 players',1,2,25,NULL,25,NULL,20),

    -- 17-24 players (CORRECTED: 3rd place 65→60)
    ('std monthly 17-24 players',1,2,1,1,17,24,75),
    ('std monthly 17-24 players',1,2,2,2,17,24,65),
    ('std monthly 17-24 players',1,2,3,3,17,24,60),
    ('std monthly 17-24 players',1,2,4,4,17,24,55),
    ('std monthly 17-24 players',1,2,5,6,17,24,50),
    ('std monthly 17-24 players',1,2,7,8,17,24,40),
    ('std monthly 17-24 players',1,2,9,12,17,24,40),
    ('std monthly 17-24 players',1,2,13,16,17,24,30),
    ('std monthly 17-24 players',1,2,17,24,17,24,20),

    -- 8-16 players (CORRECTED: 3rd place 60→55)
    ('std monthly 8-16 players',1,2,1,1,8,16,70),
    ('std monthly 8-16 players',1,2,2,2,8,16,60),
    ('std monthly 8-16 players',1,2,3,3,8,16,55),
    ('std monthly 8-16 players',1,2,4,4,8,16,50),
    ('std monthly 8-16 players',1,2,5,6,8,16,45),
    ('std monthly 8-16 players',1,2,7,8,8,16,35),
    ('std monthly 8-16 players',1,2,9,12,8,16,35),
    ('std monthly 8-16 players',1,2,13,16,8,16,25),

-- STANDARD SERIES (Tier 3 equivalent - same as monthly at 80 base, rounded to 5s)
-- event_subtype_id = 5 (from event_subtypes table)
    -- 25-32 players
    ('std series 25-32 players',1,5,1,1,25,NULL,80),
    ('std series 25-32 players',1,5,2,2,25,NULL,70),
    ('std series 25-32 players',1,5,3,3,25,NULL,70),
    ('std series 25-32 players',1,5,4,4,25,NULL,60),
    ('std series 25-32 players',1,5,5,6,25,NULL,55),
    ('std series 25-32 players',1,5,7,8,25,NULL,45),
    ('std series 25-32 players',1,5,9,12,25,NULL,45),
    ('std series 25-32 players',1,5,13,16,25,NULL,35),
    ('std series 25-32 players',1,5,17,24,25,NULL,25),
    ('std series 25-32 players',1,5,25,NULL,25,NULL,20),

    -- 17-24 players (CORRECTED: 3rd place 65→60)
    ('std series 17-24 players',1,5,1,1,17,24,75),
    ('std series 17-24 players',1,5,2,2,17,24,65),
    ('std series 17-24 players',1,5,3,3,17,24,60),
    ('std series 17-24 players',1,5,4,4,17,24,55),
    ('std series 17-24 players',1,5,5,6,17,24,50),
    ('std series 17-24 players',1,5,7,8,17,24,40),
    ('std series 17-24 players',1,5,9,12,17,24,40),
    ('std series 17-24 players',1,5,13,16,17,24,30),
    ('std series 17-24 players',1,5,17,24,17,24,20),

    -- 8-16 players (CORRECTED: 3rd place 60→55)
    ('std series 8-16 players',1,5,1,1,8,16,70),
    ('std series 8-16 players',1,5,2,2,8,16,60),
    ('std series 8-16 players',1,5,3,3,8,16,55),
    ('std series 8-16 players',1,5,4,4,8,16,50),
    ('std series 8-16 players',1,5,5,6,8,16,45),
    ('std series 8-16 players',1,5,7,8,8,16,35),
    ('std series 8-16 players',1,5,9,12,8,16,35),
    ('std series 8-16 players',1,5,13,16,8,16,25),

-- STANDARD WEEKLY (Tier 2 equivalent - 75% of 50 base, rounded to 5s)  
-- event_subtype_id = 1 (from event_subtypes table)
    -- 25-32 players
    ('std weekly 25-32 players',1,1,1,1,25,NULL,40),
    ('std weekly 25-32 players',1,1,2,2,25,NULL,35),
    ('std weekly 25-32 players',1,1,3,3,25,NULL,30),
    ('std weekly 25-32 players',1,1,4,4,25,NULL,25),
    ('std weekly 25-32 players',1,1,5,6,25,NULL,25),
    ('std weekly 25-32 players',1,1,7,8,25,NULL,20),
    ('std weekly 25-32 players',1,1,9,12,25,NULL,15),
    ('std weekly 25-32 players',1,1,13,16,25,NULL,10),
    ('std weekly 25-32 players',1,1,17,24,25,NULL,10),
    ('std weekly 25-32 players',1,1,25,NULL,25,NULL,5),

    -- 17-24 players (CORRECTED: 4th place 20→18)
    ('std weekly 17-24 players',1,1,1,1,17,24,35),
    ('std weekly 17-24 players',1,1,2,2,17,24,30),
    ('std weekly 17-24 players',1,1,3,3,17,24,25),
    ('std weekly 17-24 players',1,1,4,4,17,24,18),
    ('std weekly 17-24 players',1,1,5,6,17,24,20),
    ('std weekly 17-24 players',1,1,7,8,17,24,15),
    ('std weekly 17-24 players',1,1,9,12,17,24,10),
    ('std weekly 17-24 players',1,1,13,16,17,24,5),
    ('std weekly 17-24 players',1,1,17,24,17,24,5),

    -- 8-16 players (CORRECTED: 5-6th place 15→12)
    ('std weekly 8-16 players',1,1,1,1,8,16,30),
    ('std weekly 8-16 players',1,1,2,2,8,16,25),
    ('std weekly 8-16 players',1,1,3,3,8,16,20),
    ('std weekly 8-16 players',1,1,4,4,8,16,15),
    ('std weekly 8-16 players',1,1,5,6,8,16,12),
    ('std weekly 8-16 players',1,1,7,8,8,16,10),
    ('std weekly 8-16 players',1,1,9,12,8,16,5),
    ('std weekly 8-16 players',1,1,13,16,8,16,5),

-- STANDARD LEAGUE (Tier 1 equivalent - 75% of 50 base, slightly lower, rounded to 5s)
-- event_subtype_id = 3 (from event_subtypes table)  
    -- 25-32 players
    ('std league 25-32 players',1,3,1,1,25,NULL,35),
    ('std league 25-32 players',1,3,2,2,25,NULL,30),
    ('std league 25-32 players',1,3,3,3,25,NULL,30),
    ('std league 25-32 players',1,3,4,4,25,NULL,25),
    ('std league 25-32 players',1,3,5,6,25,NULL,20),
    ('std league 25-32 players',1,3,7,8,25,NULL,15),
    ('std league 25-32 players',1,3,9,12,25,NULL,15),
    ('std league 25-32 players',1,3,13,16,25,NULL,10),
    ('std league 25-32 players',1,3,17,24,25,NULL,5),
    ('std league 25-32 players',1,3,25,NULL,25,NULL,5),

    -- 17-24 players (CORRECTED: 3rd place 25→22)
    ('std league 17-24 players',1,3,1,1,17,24,30),
    ('std league 17-24 players',1,3,2,2,17,24,25),
    ('std league 17-24 players',1,3,3,3,17,24,22),
    ('std league 17-24 players',1,3,4,4,17,24,20),
    ('std league 17-24 players',1,3,5,6,17,24,15),
    ('std league 17-24 players',1,3,7,8,17,24,10),
    ('std league 17-24 players',1,3,9,12,17,24,10),
    ('std league 17-24 players',1,3,13,16,17,24,5),
    ('std league 17-24 players',1,3,17,24,17,24,5),

    -- 8-16 players (CORRECTED: 3rd place 20→18)
    ('std league 8-16 players',1,3,1,1,8,16,25),
    ('std league 8-16 players',1,3,2,2,8,16,20),
    ('std league 8-16 players',1,3,3,3,8,16,18),
    ('std league 8-16 players',1,3,4,4,8,16,15),
    ('std league 8-16 players',1,3,5,6,8,16,10),
    ('std league 8-16 players',1,3,7,8,8,16,5),
    ('std league 8-16 players',1,3,9,12,8,16,5),
    ('std league 8-16 players',1,3,13,16,8,16,5);

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