-- Insert event_types
-- INSERT INTO event_types (name) VALUES ('weekly');
-- INSERT INTO event_types (name) VALUES ('monthly');
-- INSERT INTO event_types (name) VALUES ('major');
-- INSERT INTO event_types (name) VALUES ('series');


-- Default subtypes (no specific pattern)
INSERT INTO event_subtypes (name, description, event_type_id, day_of_week, week_position, tier)
VALUES 
  ('Standard Weekly', 'Standard Weekly', 1, NULL, NULL, NULL),
  ('Standard Monthly', 'Standard Monthly', 2, NULL, NULL, NULL),
  ('Standard League', 'Standard League', 3, NULL, NULL, NULL),
  ('Standard Major', 'Standard Major', 4, NULL, NULL, NULL),
  ('Standard Series', 'Standard Series', 5, NULL, NULL, NULL);

-- Specific subtypes
INSERT INTO event_subtypes (name, description, event_type_id, day_of_week, week_position, tier)
VALUES("First Sunday Main Event", "Highest priority to ensure field sells out every time. This is the main event.",2,0,1,4),
("Sunday", "Second highest priority to retain monthly Sunday players", 1, 0, NULL, 3),
("Monday Chip Tournament", "Lowest priority points because this event is already highly popular", 1, 1, NULL, 1),
("Tuesday Split Bracket", "Low priority points because this event is already somewhat popular", 1, 2, NULL, 2),
("Friday Night Tournament", "Low priority points because this event is already highly popular", 1, 5, NULL, 2),
("Saturday Night Tournament", "Second highest priority because this tournament needs a major boost", 1, 6, NULL, 3)

