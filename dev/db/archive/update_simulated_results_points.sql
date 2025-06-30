UPDATE results
SET points = (
  CASE 
    WHEN event_types.name = 'weekly' THEN ROUND((
      CASE 
        WHEN results.position_std = 1 THEN 10
        WHEN results.position_std = 2 THEN 8
        WHEN results.position_std = 3 THEN 6
        WHEN results.position_std = 4 THEN 5
        WHEN results.position_std IN (5,6) THEN 3
        WHEN results.position_std IN (7,8) THEN 2
        WHEN results.position_std >= 9 THEN 1
        ELSE 0
      END
    ) *
      CASE 
        WHEN events.roster >= 32 THEN 1.5
        WHEN events.roster >= 17 THEN 1.25
        ELSE 1.0
      END
    )
    WHEN event_types.name = 'monthly' THEN ROUND((
      CASE 
        WHEN results.position_std = 1 THEN 15
        WHEN results.position_std = 2 THEN 12
        WHEN results.position_std = 3 THEN 10
        WHEN results.position_std = 4 THEN 8
        WHEN results.position_std IN (5,6) THEN 6
        WHEN results.position_std IN (7,8) THEN 4
        WHEN results.position_std >= 9 THEN 2
        ELSE 0
      END
    ) *
      CASE 
        WHEN events.roster >= 32 THEN 1.5
        WHEN events.roster >= 17 THEN 1.25
        ELSE 1.0
      END
    )
    ELSE NULL
  END
)
FROM events
JOIN event_types ON events.event_type_id = event_types.id
WHERE results.event_id = events.id;
