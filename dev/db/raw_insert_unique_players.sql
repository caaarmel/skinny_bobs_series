INSERT INTO players (full_name, first_name, last_name, alias)
SELECT DISTINCT
  sr.FULL_NAME,
  sr.FIRST_NAME,
  sr.LAST_NAME,
  sr.ALIAS
FROM staging_results sr
WHERE sr.FULL_NAME IS NOT NULL
AND sr.processed_datetime is null
-- Note: The UNIQUE constraint on full_name in the players table will prevent duplicate entries.