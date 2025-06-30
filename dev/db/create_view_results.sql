CREATE VIEW results AS
SELECT
  sr.id AS id,  -- same as source_id
  p.id AS player_id,
  e.id AS event_id,
  sr.PRIZE AS prize,
  sr.points AS points,
  sr.POSITION AS position_orig,
  sr.POSITION_STD AS position_std,
  sr.id AS source_id,
  sr.processed_datetime AS created_at,
  NULL AS updated_at  -- optional if you don’t track updates
FROM staging_results sr
JOIN players p ON p.full_name = sr.FULL_NAME
JOIN events e ON e.tourney_slug = sr.TOURNEY AND e.date = sr.DATE
--WHERE sr.processed_datetime IS NOT NULL;
