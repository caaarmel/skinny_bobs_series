import sqlite3
import os 
import shutil 
import re #regex
from datetime import datetime
from config import DB_PATH, RAW_TXT_DIR, ARCHIVE_DIR

# Utility to convert string to float safely
def  safe_float(val):
    try: # Convert to float
        return float(val)
    except ValueError: 
        return None 
    
# Normalize Tournament Name
def normalize_tourney_name(tourney):
    # Remove trailing date patterns (e.g., "_01-07-2025" or " 01/07/25") from the tournament name
    base_name = re.sub(r'[_\s/]?(?:\d{1,2}[-/])?\d{1,2}[-/]\d{2,4}$|[_\s/]?\d{6}$', '', tourney)
    base_name = base_name.replace("_", " ")
    
    # If base_name is all upper or all lower, convert to title case
    if base_name.isupper() or base_name.islower():
        base_name = base_name.title()
    return base_name


# Normalize date (Jan 07/25 -> 2025-01-07)
def normalize_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%b %d/%y").strftime("%Y-%m-%d")
    except ValueError:
        return None

# Normalize position (eg 5-6 -> 5)
def normalize_position(position,roster_val): 
    if position == "WINNER":
        return 1
    elif position == "2nd":
        return 2
    elif position == "3rd":
        return 3
    elif position == "4th":
        return 4        
    else:
        try:
            if int(position.split("-")[0]) > roster_val:
                return roster_val
            else:
                return int(position.split("-")[0])
        except ValueError:
            return None
    
# Normalize full name (eg "Bob Smith" -> "Bob Smith")
def normalize_name(name):
    if name.isupper() and len(name) < 2: 
        return name.title() 
    elif name.islower():
        return name.title()
    return name

# split the names to first/second
def split_name(full_name):
    parts = full_name.strip().split()
    if len(parts) < 2:
        return (parts[0], "")  # Single name case
    return (" ".join(parts[:-1]), parts[-1])

# Connect to DB and process
def transform_records():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM source_raw_results")
    rows = cur.fetchall() 

    staged_files = set()  # To track staged files

    for row in rows:
        (
            id, 
            tourney, 
            date, 
            game, 
            format, 
            full_name, 
            alias, 
            skill,
            prize,
            points,
            position,
            roster,
            file_name,
            insert_date
        ) = row # Unpack the row

        # Transform
        cleaned_tourney = normalize_tourney_name(tourney)
        formatted_date = normalize_date(date)
        normalized_name = normalize_name(full_name)
        first_name, last_name = split_name(normalized_name)
        prize_val = safe_float(prize)
        roster_val = safe_float(roster)
        position_std = normalize_position(position, roster_val)

        try:
            cur.execute("""
                INSERT INTO staging_results(
                        tourney,
                        tourney_clean,
                        date,
                        game,
                        format,
                        full_name,
                        full_name_clean,
                        first_name,
                        last_name,
                        alias,
                        skill,
                        prize,
                        position,
                        position_std,
                        roster,
                        source_id,
                        created_at
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
                """, (
                    tourney,
                    cleaned_tourney,
                    formatted_date,
                    game,
                    format,
                    full_name,
                    normalized_name,
                    first_name,
                    last_name,
                    alias,
                    skill,
                    prize_val,
                    position,
                    position_std,
                    roster_val,
                    id,
                    datetime.now().isoformat()
                ))
            staged_files.add(file_name)
        except sqlite3.IntegrityError:
            print(f"Dupe skipped: {full_name} in {tourney}")
            continue

    conn.commit()
    conn.close()

    # ARCHIVE
    for f in staged_files:
        source_path = os.path.join(RAW_TXT_DIR, f)
        dest_path = os.path.join(ARCHIVE_DIR, f)
        if os.path.exists(source_path):
            shutil.move(source_path, dest_path)
            print(f"Completed. Moved {f} to archive.")

if __name__ == "__main__":
    transform_records()