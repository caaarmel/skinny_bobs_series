DROP TABLE IF EXISTS source_raw_results;

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
