CREATE VIEW season_2025_standings AS
SELECT
  p.full_name,
  COUNT(r.id) AS total_events,
  
  COUNT(CASE WHEN r.position_std = 1 THEN 1 END) AS top_finish,
  COUNT(CASE WHEN r.position_std <= 3 THEN 1 END) AS top_3_finish,
  
  SUM(r.points) AS total_points,
  date(MAX(e.date)) AS last_played

FROM results r
JOIN players p ON r.player_id = p.id
JOIN events e ON r.event_id = e.id
JOIN event_types et ON e.event_type_id = et.id

WHERE e.season_id = 1

GROUP BY p.full_name
ORDER BY total_points DESC NULLS LAST, top_finish DESC, top_3_finish DESC;
