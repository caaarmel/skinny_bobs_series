

-- event_trait_assignments table
CREATE TABLE IF NOT EXISTS event_trait_assignments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  trait_id INTEGER NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT,
  FOREIGN KEY (event_id) REFERENCES events(id),
  FOREIGN KEY (trait_id) REFERENCES event_traits(id)
);

-- event_traits table
CREATE TABLE IF NOT EXISTS event_traits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT
);


-- event_types table
CREATE TABLE IF NOT EXISTS event_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  comments TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT
);

-- events table
/*
drop table events;
*/
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tourney_slug TEXT NOT NULL,            -- slug version of tourney name (e.g. 'tuesday-weekly')
  tourney_name TEXT NOT NULL,            -- original name from results or import
  date TEXT NOT NULL,                    -- ISO format preferred
  game TEXT,                             -- e.g., '9-ball'
  roster INTEGER,                        -- number of players
  season_id INTEGER NOT NULL,
  event_type_id INTEGER,        -- general type: weekly, monthly, etc.
  event_subtype_id INTEGER,     -- more specific: 'Tuesday Weekly', 'Friday Chip'
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT,

  UNIQUE (tourney_slug, date),

  FOREIGN KEY (season_id) REFERENCES seasons(id),
  FOREIGN KEY (event_type_id) REFERENCES event_types(id),
  FOREIGN KEY (event_subtype_id) REFERENCES event_subtypes(id)
);


-- event_subtypes
/*
drop table event_subtypes
*/
CREATE TABLE IF NOT EXISTS event_subtypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,               -- e.g. 'Tuesday Weekly'
    description TEXT, 
    event_type_id INTEGER NOT NULL,

    day_of_week INTEGER,                     --  0 = Sunday to 6 = Saturday
    week_position INTEGER,                   -- 1 = 1st week, 2 = 2nd, ..., 5 = Last

    tier INT DEFAULT 0,

    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT,

    UNIQUE(name, day_of_week, week_position)
    FOREIGN KEY (event_type_id) REFERENCES event_types(id)
);


-- players table
CREATE TABLE IF NOT EXISTS players (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  alias TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT,
  UNIQUE (full_name)
);

-- point_structures
CREATE TABLE IF NOT EXISTS point_structures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id_start INTEGER NOT NULL,
    season_id_end INTEGER,
    event_subtype_id INTEGER NOT NULL,
    min_position INTEGER NOT NULL,       -- e.g. 1, 2, 3, 4, 5, 7, 9, 13
    max_position INTEGER,       -- e.g. 1, 2, 3, 4, 5, 7, 9, 13
    min_players INTEGER NOT NULL DEFAULT 0,        -- inclusive
    max_players INTEGER,                 -- NULL = no upper limit
    points_awarded INTEGER NOT NULL,

    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT,

    UNIQUE(season_id_start, event_subtype_id, min_position, max_position, min_players, max_players),
    FOREIGN KEY (event_subtype_id) REFERENCES event_subtypes(id)
    FOREIGN KEY (season_id_start) REFERENCES seasons(id)
    FOREIGN KEY (season_id_end) REFERENCES seasons(id)
);


-- -- results table
-- CREATE TABLE if NOT EXISTS results (
--   id INTEGER PRIMARY KEY,
--   player_id INTEGER NOT NULL,
--   event_id INTEGER NOT NULL,
--   prize REAL,
--   points INTEGER,
--   position_orig TEXT,
--   position_std INTEGER,
--   source_id INTEGER NOT NULL,
--   created_at TEXT DEFAULT (datetime('now')),
--   updated_at TEXT,
--   UNIQUE (player_id, event_id),
--   FOREIGN KEY (player_id) REFERENCES players(id),
--   FOREIGN KEY (event_id) REFERENCES events(id),
--   FOREIGN KEY (source_id) REFERENCES source_raw_results(id)
-- );


-- seasons table
CREATE TABLE IF NOT EXISTS seasons (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  year INTEGER NOT NULL,
  start_date TEXT,
  end_date TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT
);


