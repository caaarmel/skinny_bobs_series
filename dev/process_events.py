import sqlite3
from datetime import datetime
from config import DB_PATH

CONFIDENCE_THRESHOLD = 0.6 # >= 0.6 auto-assign, < 0.6 needs review

# Lookup tables - loaded once at startup
SUBTYPE_IDS = {}
TYPE_IDS = {}

def load_lookup_tables():
    # Load event type and subtype IDs once at startup
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Load event subtypes
    cur.execute("SELECT id, name FROM event_subtypes")
    for id, name in cur.fetchall():
        SUBTYPE_IDS[name] = id

    # Load event types
    cur.execute("SELECT id, name FROM event_types")
    for id, name in cur.fetchall():
        TYPE_IDS[name] = id

    conn.close()

    print(f"Loaded {len(SUBTYPE_IDS)} subtypes and {len(TYPE_IDS)} types")
    return len(SUBTYPE_IDS) > 0 and len(TYPE_IDS) > 0

def get_unprocessed_events():
    # Get unique events from staging that haven't been processed yet
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Group staging records by unique event
    cur.execute("""
                
        SELECT
            tourney,
            tourney_clean,
            date,
            game,
            MAX(roster) as roster
        FROM staging_results
        WHERE processed_datetime is NULL
        GROUP BY tourney, date, game
        ORDER BY date, tourney
    """)

    events = cur.fetchall()
    conn.close()
    return events

def get_season_for_date(event_date):
    # Find the season that contains this date
    conn = sqlite3.connect(DB_PATH)
    cur =conn.cursor()

    cur.execute("""
        SELECT id, name
        FROM seasons
        WHERE date(?) BETWEEN date(start_date) AND (end_date) 
    
    """, (event_date,))

    result = cur.fetchone()
    conn.close()

    return result # Returns (season_id, season_name)

def event_exists(tourney_slug, date):
    # Check if event already exists
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM events
        WHERE tourney_slug = ? AND date = ?
    """, (tourney_slug, date))

    result = cur.fetchone()
    conn.close()

    return result is not None

def get_weekday_from_date(date_str):
    # Get weekday number form date string (0=Sunday, 6 = Saturday)
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        # convert Python weekday (0=Monday) to our format (0=Sunday)
        python_weekday = dt.weekday()
        cur_weekday = (python_weekday + 1) % 7
        return cur_weekday
    except ValueError:
        return None
    
def get_weekday_name_from_date(weekday_number):
    # Get the weekday name from the weekday number (0=Sunday, 6 = Saturday)
    try:
        if weekday_number == 0:
            return "Sunday"
        elif weekday_number == 1:
            return "Monday"
        elif weekday_number == 2:
            return "Tuesday"
        elif weekday_number == 3:
            return "Wednesday"
        elif weekday_number == 4:
            return "Thursday"
        elif weekday_number == 5:
            return "Friday"
        elif weekday_number == 6:
            return "Saturday"
        else:
            return "???"
    except ValueError:
        return None
    
def is_first_week_of_month(date_str):
    # Check if date falls in first week of month
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        # calculate week position (day - 1) // 7 + 1
        week_position = (dt.day - 1) // 7 + 1
        return week_position == 1
    except ValueError:
        return False
    
def classify_event_subtype(tourney_name, tourney_clean, date):
    """
    Classify event subtype with confidence scoring
    Returns: (subtype_id, event_type_id, confidence, notes)
    """

    tourney_lower = tourney_clean.lower()
    weekday = get_weekday_from_date(date)
    is_first_week = is_first_week_of_month(date)
    weekday_name = get_weekday_name_from_date(weekday)

    # Perfect matches (1.0 confidence)
    if "first sunday" in tourney_lower and weekday == 0 and is_first_week:
        return (SUBTYPE_IDS.get("First Sunday Main Event"),
                TYPE_IDS.get("monthly"),
                1.0, "Perfect match: First Sunday Main Event")
    
    if ("tue" in tourney_lower or "tuesday" in tourney_lower) and "split" in tourney_lower and weekday == 2:
        return (SUBTYPE_IDS.get("Tuesday Split Bracket"),
                TYPE_IDS.get("weekly"),
                0.8, "High confidence: Tuesday Split Bracket")
        
    # High Confidence matches (0.8+)
    if "chip" in tourney_lower and weekday == 1:
        return (SUBTYPE_IDS.get("Monday Chip Tournament"),
                TYPE_IDS.get("weekly"),
                0.9, "High confidence: Monday Chip Tournament"
                )
        
    if ("fri" in tourney_lower or "friday" in tourney_lower) and "week" in tourney_lower and weekday == 5:
        return (SUBTYPE_IDS.get("Friday Night Tournament"),
                TYPE_IDS.get("weekly"),
                0.8, "High confidence: Friday Night tournament")
    
    if ("sat" in tourney_lower or "saturday" in tourney_lower) and ("week" in tourney_lower or "mini" in tourney_lower) and weekday == 6:
        return (SUBTYPE_IDS.get("Saturday Night Tournament"),
                TYPE_IDS.get("weekly"),
                0.8, "High confidence: Saturday Night Tournament")
    
    if ("sun" in tourney_lower or "sunday" in tourney_lower) and ("week" in tourney_lower) and weekday == 0:
        return (SUBTYPE_IDS.get("Sunday"),
                TYPE_IDS.get("weekly"),
                0.8, "High confidence: Sunday weekly")
    
    # Medium Confidence
    if weekday == 0 and is_first_week: # Sunday, first week but name unclear
        return (SUBTYPE_IDS.get("First Sunday Main Event"),
                TYPE_IDS.get("monthly"),
                0.6, "Medium confidence: First Sunday by date, unclear name"
        )
    
    """ Low Confidence, applying standard event_types with no specific (standard) event_subtypes """
    # Weekly patterns
    if any(word in tourney_lower for word in ["weekly", "week"]):
        return(SUBTYPE_IDS.get("Standard Weekly"),
               TYPE_IDS.get("weekly"),
               0.4, f"Low confidence, standard weekly {weekday_name} event based on tourney name"
            )

    if 1 <= weekday <= 5 and not(any(word in tourney_lower for word in ["month"])):
        return(SUBTYPE_IDS.get("Standard Weekly"),
               TYPE_IDS.get("weekly"),
               0.4, f"Low confidence, standard weekly {weekday_name} event based on tourney date"
            )
    
    # Major patterns
    if (weekday == 6 or weekday == 0) and not(any(word in tourney_lower for word in ["week", "night", "mini"])) and any(word in tourney_lower for word in ["classic", "texas open"]): 
        return(SUBTYPE_IDS.get("Standard Major"),
               TYPE_IDS.get("major"),
               0.4, f"Low confidence, standard major {weekday_name} event based on tourney date and name")
    
    # Series Patterns
    if (weekday == 6 or weekday == 0) and not(any(word in tourney_lower for word in ["week", "night", "mini"])) and any(word in tourney_lower for word in ["series"]): 
        return(SUBTYPE_IDS.get("Standard Series"),
               TYPE_IDS.get("series"),
               0.4, f"Low confidence, new skinny bob series {weekday_name} event based on tourney date and name")
    
    # Monthly patterns
    if (weekday == 6 or weekday == 0) and not(any(word in tourney_lower for word in ["week", "night", "mini"])): #checks weekend that doesn't say "weekly"
        return(SUBTYPE_IDS.get("Standard Monthly"),
               TYPE_IDS.get("monthly"),
               0.4, f"Low confidence, standard monthly {weekday_name} event based on tourney date and name")
    
    # Very uncertain (0.2)
    return (None, None, 0.2, "Very uncertain: unable to classify")

def create_event(tourney_slug, tourney_name, date, game, roster, season_id, 
                 event_type_id, event_subtype_id, confidence, notes):
    # Create a new event record
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Determine review status basedon confidence
    needs_review = 1 if confidence < CONFIDENCE_THRESHOLD else 0

    try:
        cur.execute("""
            INSERT INTO events (
                tourney_slug, 
                tourney_name, 
                date, 
                game, 
                roster, 
                season_id,
                event_type_id, 
                event_subtype_id,
                manual_override,
                classification_confidence,
                needs_review,
                classification_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
                """, (tourney_slug, tourney_name, date, game, roster, season_id, 
                      event_type_id, event_subtype_id, confidence, needs_review, notes))
        
        event_id = cur.lastrowid
        conn.commit()

        status = "AUTO-ASSIGNED" if needs_review == 0 else "NEEDS REVIEW"
        print(f"Created event: {tourney_name} {date} - {status} (confidence: {confidence:.1f})")

        return event_id
    
    except sqlite3.IntegrityError:
        print(f"Event already exists: {tourney_name} on {date}")
        return None
    finally:
        conn.close()

def mark_records_processed():
    # Mark all staging records as processed after successful event creation
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                UPDATE staging_results
                SET processed_datetime = ?
                WHERE processed_datetime IS NULL
        """, (datetime.now().isoformat(),))
    
    updated_count = cur.rowcount
    conn.commit()
    conn.close()

    print(f"Marked {updated_count} staging records as processed")

def process_events():
    # Main function to process all unprocessed event
    print("Starting event processing...")

    # Load lookup tables first
    if not load_lookup_tables():
        print(f"Failed to load lookup tables. Check event_types and event_subtypes tables")
        return
    
    unprocessed_events = get_unprocessed_events()
    print(f"Found {len(unprocessed_events)} unique events to process")

    created_count = 0
    duplicate_count = 0
    review_count = 0 
    auto_assigned_count = 0
    no_season_count = 0

    for tourney, tourney_clean, date, game, roster in unprocessed_events:
        # Skip if event already exists
        if event_exists(tourney, date):
            duplicate_count +=1
            continue

        # Get season for this date
        season_result = get_season_for_date(date)
        if not season_result:
            print(f"No season found for date {date}, skipping event: {tourney_clean}")
            no_season_count +=1
            continue

        season_id, season_name = season_result

        # Classify event
        subtype_id, type_id, confidence, notes = classify_event_subtype(
            tourney, tourney_clean,date
            )
        
        # Create the event
        event_id = create_event(
            tourney,  # tourney_slug
            tourney_clean,
            date,
            game,
            roster,
            season_id,
            type_id, # event_type_id
            subtype_id, # event_subtype_id
            confidence,
            notes
        )

        if event_id:
            created_count += 1
            if confidence >= CONFIDENCE_THRESHOLD:
                auto_assigned_count +=1
            else:
                review_count += 1

    print(f"\nEvent processing complete:")
    print(f"\nCreated: {created_count}")
    print(f"\nAlready existed: {duplicate_count}")
    print(f"\nAuto-assigned: {auto_assigned_count}")
    print(f"\nNeed review: {review_count}")
    print(f"\nNo season found: {no_season_count}")

    if created_count > 0:
        print(f"\nMarking staging records as processed...")
        mark_records_processed()

    if review_count > 0:
        print(f"\n{review_count} events need manual review")
        print("Query: SELECT * FROM events WHERE needs_review = 1")

if __name__ == "__main__":
    process_events()