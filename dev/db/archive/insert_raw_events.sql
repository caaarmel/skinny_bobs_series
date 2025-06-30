SELECT 
  e.id AS event_id,
  r.DIVISION,
  MAX(r.IS_HANDICAP) AS is_handicap
FROM events e
JOIN source_raw_results r 
  ON r.tourney = e.tourney AND r.DATE = e.date
GROUP BY e.id, r.DIVISION
HAVING MAX(r.IS_HANDICAP) = 1 OR lower(r.DIVISION) = 'womens';

