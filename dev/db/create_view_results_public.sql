CREATE IF NOT EXISTS VIEW view_results_public AS
SELECT
  p.full_name AS "Player",
  e.tourney_name AS "Tournament",
  strftime('%Y-%m-%d', e.date) AS "Date",
  sr.POSITION_STD AS "Place",
  sr.points AS "Points",
  sr.PRIZE AS "Prize",
  et.name AS "Event Type"
FROM staging_results sr
JOIN players p ON p.full_name = sr.FULL_NAME
JOIN events e ON e.tourney_slug = sr.TOURNEY AND e.date = sr.DATE
JOIN event_types et ON et.id = e.event_type_id
--WHERE sr.processed_datetime IS NOT NULL
ORDER BY e.date DESC;
