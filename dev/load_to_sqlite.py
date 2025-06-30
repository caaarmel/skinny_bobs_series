import os # Basic OS tools
import sqlite3 #SQLite database operations
import shutil # File operations
from datetime import datetime # For timestamping
from config import RAW_TXT_DIR, ARCHIVE_DIR, DB_PATH # Import paths from config


TABLE_NAME = "source_raw_results"

def ensure_directories():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists

def insert_into_db(txt_file_path):
    conn = sqlite3.connect(DB_PATH) # Connect to the SQLite database
    cur = conn.cursor() # Create a cursor object to execute SQL commands

    with open(txt_file_path, "r", encoding="utf-8") as f: # Open the text file for reading
        lines = f.readlines() # Read all lines from the file

    # First line might be the heading like final results, so skip this if not tab-separated
    start = 0
    if "\t" not in lines[0]: # Check if the first line is not tab-separated
        start = 1

    for line in lines[start:]: # Iterate over each line starting from the second line if the first is a heading
        row = line.strip().split("\t") # Split the line into columns using tab as the delimiter
        if len(row) != 11 or row[0].strip().upper() == "TOURNEY":
            continue # Skip rows that do not have at least 11 columns or if the first column is "TOURNEY"

        cur.execute(f"""
            INSERT OR IGNORE INTO {TABLE_NAME} (
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
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row + [os.path.basename(txt_file_path), datetime.now().isoformat()]) # Insert the row into the database
    conn.commit() # Commit the transaction to save changes
    conn.close() # Close the database connection

def main():
    ensure_directories()

    txt_files = [f for f in os.listdir(RAW_TXT_DIR) if f.lower().endswith(".txt")] # List all text files in the raw directory

    for filename in txt_files: # Iterate over each text file
        file_path = os.path.join(RAW_TXT_DIR, filename) # Get the full path of the text file    
        print(f"Processing file: {file_path}")

        try:
            insert_into_db(file_path) # Insert the data from the text file into the database
            print(f" loading {filename} into database: {TABLE_NAME}")
        except Exception as e: # Catch any exceptions that occur during processing
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main() # Run the main function when the script is executed
