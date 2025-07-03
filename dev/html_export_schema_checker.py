import sqlite3
import json
import os
from datetime import datetime
from config import DB_PATH, OFFLINE_HTML_DIR

def check_database_schema():
    """
    Check what tables and columns actually exist in your database
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("🔍 Checking database schema...")
    
    # Get all tables
    tables_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    tables = [row[0] for row in cur.execute(tables_query).fetchall()]
    
    print(f"📋 Tables found: {tables}")
    
    # Get all views
    views_query = "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"
    views = [row[0] for row in cur.execute(views_query).fetchall()]
    
    print(f"👁️  Views found: {views}")
    
    # Check each table/view structure
    for table_name in tables + views:
        try:
            columns_query = f"PRAGMA table_info({table_name})"
            columns = cur.execute(columns_query).fetchall()
            print(f"\n📊 {table_name} columns:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
        except Exception as e:
            print(f"   ❌ Error checking {table_name}: {e}")
    
    conn.close()
    return tables, views

if __name__ == "__main__":
    check_database_schema()