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

def export_standings_html_v2():
    """
    Generate HTML export based on your actual database schema
    """
    
    # First check what we're working with
    tables, views = check_database_schema()
    
    # Ensure output directory exists
    os.makedirs(OFFLINE_HTML_DIR, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    cur = conn.cursor()
    
    try:
        # Try to get data from the most likely tables/views
        
        # Check if we have a results view or table
        if 'results' in views or 'results' in tables:
            print("✅ Using 'results' view/table")
            
            # Get all data we need from the results view
            results_query = """
            SELECT 
                r.id,
                r.player_id,
                r.event_id, 
                r.prize,
                r.points,
                r.position_orig,
                r.position_std
            FROM results r
            """
            results = [dict(row) for row in cur.execute(results_query).fetchall()]
            
        elif 'staging_results' in tables:
            print("✅ Using 'staging_results' table")
            
            # Get data from staging_results
            results_query = """
            SELECT 
                ID as id,
                full_name as player_name,
                tourney,
                date,
                prize,
                points,
                position as position_orig,
                position_std
            FROM staging_results
            WHERE processed_datetime IS NOT NULL
            """
            results = [dict(row) for row in cur.execute(results_query).fetchall()]
            
        else:
            raise Exception("Could not find results data in database")
        
        # Get players data
        if 'players' in tables:
            players_query = """
            SELECT id, full_name, first_name, last_name, alias 
            FROM players 
            ORDER BY id
            """
            players = [dict(row) for row in cur.execute(players_query).fetchall()]
        else:
            # Create players from staging_results
            print("⚠️  No players table found, extracting from staging_results")
            players_query = """
            SELECT DISTINCT 
                full_name,
                first_name,
                last_name,
                alias
            FROM staging_results
            ORDER BY full_name
            """
            temp_players = [dict(row) for row in cur.execute(players_query).fetchall()]
            # Add IDs
            players = [dict(row, id=i+1) for i, row in enumerate(temp_players)]
        
        # Get events data
        if 'events' in tables:
            events_query = """
            SELECT id, tourney_slug as tourney, tourney_name, date, game, roster, season_id, event_type_id
            FROM events 
            ORDER BY id
            """
            events = [dict(row) for row in cur.execute(events_query).fetchall()]
        else:
            # Create events from staging_results
            print("⚠️  No events table found, extracting from staging_results")
            events_query = """
            SELECT DISTINCT 
                tourney,
                date,
                game,
                roster
            FROM staging_results
            ORDER BY date
            """
            temp_events = [dict(row) for row in cur.execute(events_query).fetchall()]
            # Add IDs and clean up
            events = []
            for i, row in enumerate(temp_events):
                events.append({
                    'id': i+1,
                    'tourney': row['tourney'],
                    'tourney_name': row['tourney'].replace('_', ' ').title(),
                    'date': row['date'],
                    'game': row['game'],
                    'roster': row['roster'],
                    'season_id': 1,
                    'event_type_id': 1
                })
        
        conn.close()
        
        print(f"📊 Data extracted:")
        print(f"   - {len(players)} players")
        print(f"   - {len(events)} events") 
        print(f"   - {len(results)} results")
        
        # If we're using staging_results, we need to create proper relationships
        if 'staging_results' in tables and 'results' not in views:
            print("🔄 Converting staging data to proper format...")
            
            # Create player lookup
            player_lookup = {p['full_name']: p['id'] for p in players}
            event_lookup = {}
            for e in events:
                key = f"{e['tourney']}-{e['date']}"
                event_lookup[key] = e['id']
            
            # Convert results to proper format
            converted_results = []
            for i, r in enumerate(results):
                player_id = player_lookup.get(r.get('player_name'))
                event_key = f"{r.get('tourney')}-{r.get('date')}"
                event_id = event_lookup.get(event_key)
                
                if player_id and event_id:
                    converted_results.append({
                        'id': i+1,
                        'player_id': player_id,
                        'event_id': event_id,
                        'prize': r.get('prize'),
                        'points': r.get('points'),
                        'position_orig': r.get('position_orig'),
                        'position_std': r.get('position_std')
                    })
            
            results = converted_results
            print(f"✅ Converted {len(results)} results with proper relationships")
        
        # Generate HTML (same as before)
        players_json = json.dumps(players, indent=0, separators=(',', ': '))
        events_json = json.dumps(events, indent=0, separators=(',', ': '))
        results_json = json.dumps(results, indent=0, separators=(',', ': '))
        
        # Generate the HTML content (same template as before)
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <title>Skinny Bob's 2025 Standings</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 2rem; table-layout: auto; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; vertical-align: top; white-space: normal; word-break: break-word; }}
    th {{ background-color: #f4f4f4; }}
    td, th {{ text-transform: none; }}
    .details {{ display: none; padding-left: 1rem; background-color: #fafafa; }}
    .expandable:hover {{ cursor: pointer; background-color: #eef; }}
    .footer {{ margin-top: 2rem; font-size: 0.9em; color: #666; }}
  </style>
</head>
<body>
  <h1>Skinny Bob's Series - 2025 Player Standings</h1>
  <p>Click on any player row to see their tournament history details.</p>
  
  <table id="standingsTable">
    <thead>
      <tr>
        <th>Player</th>
        <th>Total Points</th>
        <th>Events Played</th>
        <th>Top 3 Finishes</th>
      </tr>
    </thead>
    <tbody id="standingsBody"></tbody>
  </table>
  
  <div class="footer">
    Generated on {datetime.now().strftime('%Y-%m-%d at %I:%M %p')}
  </div>

<script>
const playersData = {players_json};
const eventsData = {events_json};
const resultsData = {results_json};

// Create lookup objects for faster access
const playersById = {{}};
const eventsById = {{}};

// Populate lookup objects
for (const p of playersData) playersById[p.id] = p;
for (const e of eventsData) eventsById[e.id] = e;

// Group results by player
const playerResults = {{}};
for (const r of resultsData) {{
  if (!playerResults[r.player_id]) playerResults[r.player_id] = [];
  playerResults[r.player_id].push(r);
}}

// Calculate standings
const standings = Object.entries(playerResults).map(([pid, rlist]) => {{
  const totalPoints = rlist.reduce((sum, r) => sum + (r.points || 0), 0);
  const eventsPlayed = rlist.length;
  const top3Count = rlist.filter(r => {{
    const pos = r.position_std;
    return typeof pos === 'number' && pos >= 1 && pos <= 3;
  }}).length;
  
  return {{
    pid,
    name: playersById[pid]?.full_name || playersById[pid]?.alias || "Unknown",
    totalPoints,
    eventsPlayed,
    top3Count,
    history: rlist.sort((a, b) => {{
      const aDate = eventsById[a.event_id]?.date || '';
      const bDate = eventsById[b.event_id]?.date || '';
      return bDate.localeCompare(aDate); // Most recent first
    }})
  }};
}});

// Sort by total points (highest first)
standings.sort((a, b) => b.totalPoints - a.totalPoints);

// Build the table
const tbody = document.getElementById('standingsBody');
standings.forEach((player, index) => {{
  // Main row (clickable)
  const tr = document.createElement('tr');
  tr.className = 'expandable';
  tr.innerHTML = `
    <td>${{player.name}}</td>
    <td>${{player.totalPoints}}</td>
    <td>${{player.eventsPlayed}}</td>
    <td>${{player.top3Count}}</td>
  `;
  
  // Details row (hidden by default)
  const details = document.createElement('tr');
  details.className = 'details';
  details.innerHTML = `
    <td colspan="4">
      <strong>Event History:</strong>
      <ul style="margin: 0.5rem 0 0 1.5rem; padding-left: 0;">
        ${{player.history.map(function(r) {{
          const e = eventsById[r.event_id];
          const date = e?.date?.split("T")[0] || "??";
          const name = e?.tourney_name || "Unknown Event";
          let place = r.position_orig;
          if (place?.toLowerCase() === "winner") {{
            place = "1st";
          }}
          const points = r.points !== undefined ? `${{r.points}} pts` : "";
          return `<li>${{date}} - ${{name}}: ${{place}}${{points ? ` (${{points}})` : ''}}</li>`;
        }}).join('')}}
      </ul>
    </td>
  `;
  
  // Add click handler to toggle details
  tr.onclick = () => {{
    details.style.display = (details.style.display === 'table-row') ? 'none' : 'table-row';
  }};
  
  // Add both rows to table
  tbody.appendChild(tr);
  tbody.appendChild(details);
}});
</script>
</body>
</html>"""
        
        # Write the HTML file
        output_file = os.path.join(OFFLINE_HTML_DIR, f"skinny_bobs_standings_{datetime.now().strftime('%Y%m%d')}.html")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Standalone HTML file generated: {output_file}")
        print(f"📁 You can now send this file to Shayla - she can open it in any web browser!")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error generating HTML: {e}")
        conn.close()
        return None

if __name__ == "__main__":
    export_standings_html_v2()