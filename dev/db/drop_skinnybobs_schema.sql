--drop_skinnybobs_schema that source from staging_results

DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS results;


/*
-- drops table that are prepopulated and used for reference

DROP TABLE IF EXISTS event_subtypes;
DROP TABLE IF EXISTS event_trait_assignments;
DROP TABLE IF EXISTS event_traits;
DROP TABLE IF EXISTS event_types;
DROP TABLE IF EXISTS point_tiers;
DROP TABLE IF EXISTS point_structures;
DROP TABLE IF EXISTS seasons;

*/


/*
-- drops tables that are generated from import files

DROP TABLE IF EXISTS source_raw_results;
DROP TABLE IF EXISTS staging_results;

*/