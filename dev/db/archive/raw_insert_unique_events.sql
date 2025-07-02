WITH resolved_event_types AS (
  SELECT 
    r.tourney,
    r.tourney_clean,
    r.DATE,
    r.GAME,
    MAX(r.ROSTER) AS roster,
    CASE
      WHEN MAX(r.IS_MONTHLY) = 1 THEN 'monthly'
      WHEN MAX(r.IS_WEEKLY) = 1 THEN 'weekly'
      WHEN MAX(r.IS_LEAGUE) = 1 THEN 'league'
      WHEN MAX(r.IS_SERIES) = 1 THEN 'series'
      WHEN MAX(r.IS_MAJOR) = 1 THEN 'major'
    END AS event_type_name
  FROM staging_results r
  WHERE r.processed_datetime is NULL
  GROUP BY r.tourney, r.DATE, r.GAME
),
with_type_ids AS (
  SELECT 
    e.*,
    et.id AS event_type_id
  FROM resolved_event_types e
  LEFT JOIN event_types et ON e.event_type_name = et.name
),
with_season_ids AS (
  SELECT 
    e.*,
    s.id AS season_id
  FROM with_type_ids e
  JOIN seasons s ON date(e.date) BETWEEN date(s.start_date) AND date(s.end_date)
)

INSERT INTO events (
  tourney_slug,
  tourney_name,
  date,
  game,
  roster,
  season_id,
  event_type_id
)
SELECT 
  e.tourney,
  e.tourney_clean AS tourney_name,
  e.date,
  e.game,
  e.roster,
  e.season_id,
  e.event_type_id
FROM with_season_ids e
