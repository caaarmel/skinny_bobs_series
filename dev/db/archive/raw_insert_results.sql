INSERT INTO results (
  player_id,
  event_id,
  prize,
  points,
  position_orig,
  position_std,
  source_id
)
SELECT
  p.id,
  e.id,
  sr.PRIZE,
  sr.points,
  sr.position,
  sr.POSITION_STD,
  sr.id
FROM staging_results sr
JOIN players p ON p.full_name = sr.FULL_NAME
JOIN events e ON e.tourney_slug = sr.TOURNEY AND e.date = sr.DATE
where sr.processed_datetime is null
