"""
EVENT TYPES SECTION
    # determine and flags per column what type of events this is
"""
weekly_event_type_keywords = ["week", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
        "tue", "wed", "thu", "fri", "sat", "sun"]

major_event_type_keywords = ["major", "texas open", "classic"]

series_event_type_keywords = ["series"]

handicap_event_type_keywords = ["handicap", "fargo", "under"]


def flag_weekly(tourney, event_date):
    if event_date:
        try:
            dt = datetime.strptime(normalize_date(event_date), "%Y-%m-%d")
            return int(dt.weekday() < 5)  # Monday=0, Sunday=6
        except ValueError:
            pass
    # fallback to keyword check in case date is missing or invalid
    t = tourney.lower()
    return int(any(keyword in t for keyword in weekly_event_type_keywords))

def flag_monthly(tourney):
    t = tourney.lower()
    return int(not any(keyword in t for keyword in weekly_event_type_keywords))

def flag_major(tourney):
    t = tourney.lower()
    return int(any(keyword in t for keyword in major_event_type_keywords))

def flag_series(tourney):
    t = tourney.lower()
    return int(any(keyword in t for keyword in series_event_type_keywords))

def flag_league(tourney):
    return int("league" in tourney.lower())

def flag_handicap(tourney):
    t= tourney.lower()
    return int(any(keyword in t for keyword in handicap_event_type_keywords))

"""
EVENT TYPES SECTION
"""