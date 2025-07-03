/*
------------------------------------------------------------------------------
-- Description:
--  Creates structure raw results(source_raw_results) and staging results after transformation

    Loaded via python: 
        load_to_sqlite.py: txt -> source_raw_results table
        transform_to_staging.py: source_raw_results -> staging_results

------------------------------------------------------------------------------
*/
DROP TABLE IF EXISTS source_raw_results;
DROP TABLE IF EXISTS staging_results;


CREATE TABLE source_raw_results (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    tourney TEXT,
    date TEXT,
    game TEXT,
    format TEXT,
    full_name TEXT,
    alias TEXT,
    skill TEXT,
    prize TEXT,
    points TEXT,
    position TEXT,
    roster TEXT,
    file_name TEXT,
    insert_date TEXT,
    UNIQUE(full_name, tourney)
);


CREATE TABLE staging_results (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    tourney TEXT,
    tourney_clean TEXT,
    date TEXT,
    game TEXT,
    format TEXT,
    full_name TEXT,
    full_name_clean TEXT,
    first_name TEXT,
    last_name TEXT,
    alias TEXT,
    skill TEXT,
    prize REAL,
    points INTEGER,
    position TEXT,
    position_std INTEGER,
    roster INTEGER,
    is_weekly BOOLEAN,
    source_id INTEGER NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    processed_datetime TEXT,

    UNIQUE (source_id),
    FOREIGN KEY (source_id) REFERENCES source_raw_results(ID)
);


