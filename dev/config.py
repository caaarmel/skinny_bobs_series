import os

# Base directory where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to import folders
IMPORT_DIR = os.path.join(BASE_DIR, "..", "import") # Import directory
RAW_HTML_DIR = os.path.join(IMPORT_DIR) # Directory for raw HTML files
RAW_TXT_DIR = os.path.join(IMPORT_DIR, "raw") # Directory for raw text files that were converted from HTML
CLEANED_TXT_DIR = os.path.join(IMPORT_DIR, "cleaned") # Directory for cleaned text files
ARCHIVE_DIR = os.path.join(IMPORT_DIR, "archived") # Directory for archived files

# Path to HTML export folder
OFFLINE_HTML_DIR = os.path.join(BASE_DIR,"sample") # Directory for offline HTML files

# Path to export folder
EXPORT_DIR = os.path.join(BASE_DIR, "..", "export") # Export directory for final output files

# Path to SQLite database
DB_PATH = os.path.join(BASE_DIR, "db", "skinnybobs.db") # SQLite database path