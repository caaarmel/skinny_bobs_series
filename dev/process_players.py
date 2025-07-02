import sqlite3 
from datetime import datetime
from config import DB_PATH

def get_unprocessed_players():
    # get unique players from staging
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT
                full_name_clean,
                first_name,
                last_name,
                alias
            FROM staging_results
            WHERE full_name_clean IS NOT NULL
            AND processed_datetime IS NULL
            ORDER BY full_name_clean                
                """)
    
    players = cur.fetchall() #
    conn.close()
    return players

def player_exists(full_name):
    # check if player already exists in players table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE full_name = ?", (full_name,)) # use parameterized query to prevent SQL injection
    result = cur.fetchone() # fetch one result
    conn.close() 

    return result is not None # return True if result is not None, else False

def create_player(full_name, first_name, last_name, alias):
    # create a new player in players table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO players (full_name, first_name, last_name, alias)
            VALUES (?,?,?,?)
        """, (full_name, first_name, last_name, alias))  # Fixed!

        player_id = cur.lastrowid
        conn.commit()
        print(f"Created player: {full_name} (ID: {player_id})")
        return player_id

    except sqlite3.IntegrityError:
        print (f"Player already exists: {full_name}")
        return None
    finally:
        conn.close()

def find_potential_duplicates(full_name, first_name, last_name):
    """
    Find potential dupes for future name clustering
    Returns list of similar players for manual review
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # simple similarity checks - enhance later
    similar_players = []

    # Check for exact first/last match with different full name
    # Check for exact first/last match with different full name
    if first_name and last_name:
        cur.execute("""
            SELECT id, full_name, first_name, last_name 
            FROM players 
            WHERE first_name = ? AND last_name = ? AND full_name != ?
        """, (first_name, last_name, full_name))
        similar_players.extend(cur.fetchall())
    
    # Check for similar full names (could add fuzzy matching here later)
    # For now, just check for substring matches
    if len(full_name) > 3:
        cur.execute("""
            SELECT id, full_name, first_name, last_name 
            FROM players 
            WHERE full_name LIKE ? AND full_name != ?
            LIMIT 5
        """, (f"%{full_name[:4]}%", full_name))
        similar_players.extend(cur.fetchall())

    conn.close()
    return similar_players

def process_players():
    # Main function to process all unprocessed players from staging_results
    print(f"Starting player processing...")

    unprocessed_players = get_unprocessed_players()
    print(f"Found {len(unprocessed_players)} unique players to process")

    created_count = 0 
    duplicate_count = 0
    potential_duplicates = []

    for full_name, first_name, last_name, alias in unprocessed_players:
        # skip if player already exists
        if player_exists(full_name):
            duplicate_count += 1
            continue

        # check for potential duplicates before creating
        similar = find_potential_duplicates(full_name, first_name, last_name)
        if similar:
            potential_duplicates.append({
                'new_player': (full_name, first_name, last_name, alias),
                'similar_existing': similar
            })

        # Create the player
        player_id = create_player(full_name, first_name, last_name, alias)
        if player_id:
            created_count += 1

    print(f"\nPlayer processing complete:")
    print(f"\nCreated: {created_count}")
    print(f"\nAlready exists: {duplicate_count}")

    # Report potential dupes for review
    if potential_duplicates:
        print(f"\n found {len(potential_duplicates)} potential dupes for review:")
        for i, dup in enumerate(potential_duplicates[:5]): #shows first five
            new_player = dup['new_player']
            similar = dup['similar_existing']
            print(f"\n{i+1}. New: {new_player[0]} | Similar: {[p[1] for p in similar]}") 
            # This section prints out a summary of potential duplicate players for manual review, showing the new player and similar existing players found in the database.

        if len(potential_duplicates) > 5:
            print(f" ... and {len(potential_duplicates) -5} more")

        print("\nConsider reviewing these for name clustering/merging")


def mark_players_processed():
    # Mark staging records as processed after successful player creation
    # leavin this blanke for now

    pass

if __name__ == "__main__":
    process_players()



