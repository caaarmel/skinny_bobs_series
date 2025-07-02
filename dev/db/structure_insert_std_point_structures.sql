-- Standard Point Structures for Generic Event Subtypes
-- These are fallback point values at 75% of the explicit tier values
-- For use when events don't have specific stakeholder-designed point structures
--
-- STANDARD POINT VALUES REFERENCE (Winner Points):
-- +------------------+--------------+--------------+--------------+
-- | Event Type       | 25-32 Player | 17-24 Player | 8-16 Players |
-- +------------------+--------------+--------------+--------------+
-- | Standard Major   |     120      |     110      |     100      |
-- | Standard Monthly |      80      |      75      |      70      |
-- | Standard Series  |      80      |      75      |      70      |
-- | Standard Weekly  |      40      |      35      |      30      |
-- | Standard League  |      35      |      30      |      25      |
-- +------------------+--------------+--------------+--------------+

-- STANDARD MAJOR (Tier 4 equivalent - 75% of 160 base, rounded to 5s)
-- event_subtype_id = 4 (from event_subtypes table)
INSERT INTO point_structures(name,season_id_start, event_subtype_id, min_position, max_position, min_players, max_players, points_awarded)
VALUES  
    -- 25-32 players
    ('major 25-32 players',1,4,1,1,25,NULL,120),
    ('major 25-32 players',1,4,2,2,25,NULL,95),
    ('major 25-32 players',1,4,3,4,25,NULL,70),
    ('major 25-32 players',1,4,5,8,25,NULL,55),
    ('major 25-32 players',1,4,9,16,25,NULL,25),
    ('major 25-32 players',1,4,17,24,25,NULL,20),
    ('major 25-32 players',1,4,25,NULL,25,NULL,15),

    -- 17-24 players  
    ('major 17-24 players',1,4,1,1,17,24,110),
    ('major 17-24 players',1,4,2,2,17,24,85),
    ('major 17-24 players',1,4,3,4,17,24,60),
    ('major 17-24 players',1,4,5,8,17,24,45),
    ('major 17-24 players',1,4,9,16,17,24,15),
    ('major 17-24 players',1,4,17,24,17,24,10),

    -- 8-16 players
    ('std major 8-16 players',1,4,1,1,8,16,100),
    ('std major 8-16 players',1,4,2,2,8,16,75),
    ('std major 8-16 players',1,4,3,4,8,16,50),
    ('std major 8-16 players',1,4,5,8,8,16,35),
    ('std major 8-16 players',1,4,9,16,8,16,5),

-- STANDARD MONTHLY (Tier 3 equivalent - upgraded to 80 base, rounded to 5s)
-- event_subtype_id = 2 (from event_subtypes table)
    -- 25-32 players
    ('std monthly 25-32 players',1,2,1,1,25,NULL,80),
    ('std monthly 25-32 players',1,2,2,2,25,NULL,70),
    ('std monthly 25-32 players',1,2,3,3,25,NULL,70),
    ('std monthly 25-32 players',1,2,4,4,25,NULL,60),
    ('std monthly 25-32 players',1,2,5,6,25,NULL,55),
    ('std monthly 25-32 players',1,2,7,8,25,NULL,45),
    ('std monthly 25-32 players',1,2,9,12,25,NULL,45),
    ('std monthly 25-32 players',1,2,13,16,25,NULL,35),
    ('std monthly 25-32 players',1,2,17,24,25,NULL,25),
    ('std monthly 25-32 players',1,2,25,NULL,25,NULL,20),

    -- 17-24 players
    ('std monthly 17-24 players',1,2,1,1,17,24,75),
    ('std monthly 17-24 players',1,2,2,2,17,24,65),
    ('std monthly 17-24 players',1,2,3,3,17,24,65),
    ('std monthly 17-24 players',1,2,4,4,17,24,55),
    ('std monthly 17-24 players',1,2,5,6,17,24,50),
    ('std monthly 17-24 players',1,2,7,8,17,24,40),
    ('std monthly 17-24 players',1,2,9,12,17,24,40),
    ('std monthly 17-24 players',1,2,13,16,17,24,30),
    ('std monthly 17-24 players',1,2,17,24,17,24,20),

    -- 8-16 players
    ('std monthly 8-16 players',1,2,1,1,8,16,70),
    ('std monthly 8-16 players',1,2,2,2,8,16,60),
    ('std monthly 8-16 players',1,2,3,3,8,16,60),
    ('std monthly 8-16 players',1,2,4,4,8,16,50),
    ('std monthly 8-16 players',1,2,5,6,8,16,45),
    ('std monthly 8-16 players',1,2,7,8,8,16,35),
    ('std monthly 8-16 players',1,2,9,12,8,16,35),
    ('std monthly 8-16 players',1,2,13,16,8,16,25),

-- STANDARD SERIES (Tier 3 equivalent - same as monthly at 80 base, rounded to 5s)
-- event_subtype_id = 5 (from event_subtypes table)
    -- 25-32 players
    ('std series 25-32 players',1,5,1,1,25,NULL,80),
    ('std series 25-32 players',1,5,2,2,25,NULL,70),
    ('std series 25-32 players',1,5,3,3,25,NULL,70),
    ('std series 25-32 players',1,5,4,4,25,NULL,60),
    ('std series 25-32 players',1,5,5,6,25,NULL,55),
    ('std series 25-32 players',1,5,7,8,25,NULL,45),
    ('std series 25-32 players',1,5,9,12,25,NULL,45),
    ('std series 25-32 players',1,5,13,16,25,NULL,35),
    ('std series 25-32 players',1,5,17,24,25,NULL,25),
    ('std series 25-32 players',1,5,25,NULL,25,NULL,20),

    -- 17-24 players
    ('std series 17-24 players',1,5,1,1,17,24,75),
    ('std series 17-24 players',1,5,2,2,17,24,65),
    ('std series 17-24 players',1,5,3,3,17,24,65),
    ('std series 17-24 players',1,5,4,4,17,24,55),
    ('std series 17-24 players',1,5,5,6,17,24,50),
    ('std series 17-24 players',1,5,7,8,17,24,40),
    ('std series 17-24 players',1,5,9,12,17,24,40),
    ('std series 17-24 players',1,5,13,16,17,24,30),
    ('std series 17-24 players',1,5,17,24,17,24,20),

    -- 8-16 players
    ('std series 8-16 players',1,5,1,1,8,16,70),
    ('std series 8-16 players',1,5,2,2,8,16,60),
    ('std series 8-16 players',1,5,3,3,8,16,60),
    ('std series 8-16 players',1,5,4,4,8,16,50),
    ('std series 8-16 players',1,5,5,6,8,16,45),
    ('std series 8-16 players',1,5,7,8,8,16,35),
    ('std series 8-16 players',1,5,9,12,8,16,35),
    ('std series 8-16 players',1,5,13,16,8,16,25),

-- STANDARD WEEKLY (Tier 2 equivalent - 75% of 50 base, rounded to 5s)  
-- event_subtype_id = 1 (from event_subtypes table)
    -- 25-32 players
    ('std weekly 25-32 players',1,1,1,1,25,NULL,40),
    ('std weekly 25-32 players',1,1,2,2,25,NULL,35),
    ('std weekly 25-32 players',1,1,3,3,25,NULL,30),
    ('std weekly 25-32 players',1,1,4,4,25,NULL,25),
    ('std weekly 25-32 players',1,1,5,6,25,NULL,25),
    ('std weekly 25-32 players',1,1,7,8,25,NULL,20),
    ('std weekly 25-32 players',1,1,9,12,25,NULL,15),
    ('std weekly 25-32 players',1,1,13,16,25,NULL,10),
    ('std weekly 25-32 players',1,1,17,24,25,NULL,10),
    ('std weekly 25-32 players',1,1,25,NULL,25,NULL,5),

    -- 17-24 players
    ('std weekly 17-24 players',1,1,1,1,17,24,35),
    ('std weekly 17-24 players',1,1,2,2,17,24,30),
    ('std weekly 17-24 players',1,1,3,3,17,24,25),
    ('std weekly 17-24 players',1,1,4,4,17,24,20),
    ('std weekly 17-24 players',1,1,5,6,17,24,20),
    ('std weekly 17-24 players',1,1,7,8,17,24,15),
    ('std weekly 17-24 players',1,1,9,12,17,24,10),
    ('std weekly 17-24 players',1,1,13,16,17,24,5),
    ('std weekly 17-24 players',1,1,17,24,17,24,5),

    -- 8-16 players
    ('std weekly 8-16 players',1,1,1,1,8,16,30),
    ('std weekly 8-16 players',1,1,2,2,8,16,25),
    ('std weekly 8-16 players',1,1,3,3,8,16,20),
    ('std weekly 8-16 players',1,1,4,4,8,16,15),
    ('std weekly 8-16 players',1,1,5,6,8,16,15),
    ('std weekly 8-16 players',1,1,7,8,8,16,10),
    ('std weekly 8-16 players',1,1,9,12,8,16,5),
    ('std weekly 8-16 players',1,1,13,16,8,16,5),

-- STANDARD LEAGUE (Tier 1 equivalent - 75% of 50 base, slightly lower, rounded to 5s)
-- event_subtype_id = 3 (from event_subtypes table)  
    -- 25-32 players
    ('std league 25-32 players',1,3,1,1,25,NULL,35),
    ('std league 25-32 players',1,3,2,2,25,NULL,30),
    ('std league 25-32 players',1,3,3,3,25,NULL,30),
    ('std league 25-32 players',1,3,4,4,25,NULL,25),
    ('std league 25-32 players',1,3,5,6,25,NULL,20),
    ('std league 25-32 players',1,3,7,8,25,NULL,15),
    ('std league 25-32 players',1,3,9,12,25,NULL,15),
    ('std league 25-32 players',1,3,13,16,25,NULL,10),
    ('std league 25-32 players',1,3,17,24,25,NULL,5),
    ('std league 25-32 players',1,3,25,NULL,25,NULL,5),

    -- 17-24 players
    ('std league 17-24 players',1,3,1,1,17,24,30),
    ('std league 17-24 players',1,3,2,2,17,24,25),
    ('std league 17-24 players',1,3,3,3,17,24,25),
    ('std league 17-24 players',1,3,4,4,17,24,20),
    ('std league 17-24 players',1,3,5,6,17,24,15),
    ('std league 17-24 players',1,3,7,8,17,24,10),
    ('std league 17-24 players',1,3,9,12,17,24,10),
    ('std league 17-24 players',1,3,13,16,17,24,5),
    ('std league 17-24 players',1,3,17,24,17,24,5),

    -- 8-16 players
    ('std league 8-16 players',1,3,1,1,8,16,25),
    ('std league 8-16 players',1,3,2,2,8,16,20),
    ('std league 8-16 players',1,3,3,3,8,16,20),
    ('std league 8-16 players',1,3,4,4,8,16,15),
    ('std league 8-16 players',1,3,5,6,8,16,10),
    ('std league 8-16 players',1,3,7,8,8,16,5),
    ('std league 8-16 players',1,3,9,12,8,16,5),
    ('std league 8-16 players',1,3,13,16,8,16,5);