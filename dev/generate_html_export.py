import sqlite3
import json
import os
from datetime import datetime
from config import DB_PATH, OFFLINE_HTML_DIR

def export_standings_html_improved():
    """
    Generate HTML export using your actual views for better data
    """
    
    # Ensure output directory exists
    os.makedirs(OFFLINE_HTML_DIR, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    print("🏆 Generating improved standings HTML using your views...")
    
    try:
        # Use your season_2025_standings view for the main standings
        standings_query = """
        SELECT 
            Player as player_name,
            "Total Points" as total_points,
            "Total Events" as total_events,
            Wins as wins,
            "Top 3" as top_3,
            "Top 8" as top_8,
            "Weekly Events" as weekly_events,
            "Monthly Events" as monthly_events,
            "Major Events" as major_events,
            "Win Rate %" as win_rate,
            "Top 3 Rate %" as top_3_rate,
            "Last Played" as last_played
        FROM season_2025_standings
        ORDER BY "Total Points" DESC
        """
        standings_data = [dict(row) for row in cur.execute(standings_query).fetchall()]
        
        # Get detailed results for history using results_public view
        results_query = """
        SELECT 
            full_name as player_name,
            tournament,
            date,
            position_orig,
            position_std,
            points_awarded as points,
            event_type_name as event_type
        FROM results_public
        ORDER BY date DESC
        """
        all_results = [dict(row) for row in cur.execute(results_query).fetchall()]
        
        conn.close()
        
        print(f"📊 Data extracted from views:")
        print(f"   - {len(standings_data)} players in standings")
        print(f"   - {len(all_results)} detailed results")
        
        # Group results by player for history
        player_history = {}
        for result in all_results:
            player = result['player_name']
            if player not in player_history:
                player_history[player] = []
            player_history[player].append(result)
        
        # Combine standings with history
        for player_data in standings_data:
            player_name = player_data['player_name']
            player_data['history'] = player_history.get(player_name, [])
        
        # Convert to JSON for embedding
        standings_json = json.dumps(standings_data, indent=0, separators=(',', ': '))
        
        # Generate enhanced HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <title>Skinny Bob's 2025 Season Standings</title>
  <style>
    body {{ 
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
      margin: 2rem; 
      background-color: #f8f9fa;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background-color: white;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }}
    h1 {{ 
      color: #2c3e50; 
      text-align: center; 
      margin-bottom: 0.5rem;
    }}
    .subtitle {{
      text-align: center;
      color: #7f8c8d;
      margin-bottom: 2rem;
      font-style: italic;
    }}
    table {{ 
      width: 100%; 
      border-collapse: collapse; 
      margin-bottom: 2rem; 
    }}
    th, td {{ 
      border: 1px solid #ddd; 
      padding: 0.75rem; 
      text-align: left; 
      vertical-align: top; 
    }}
    th {{ 
      background-color: #34495e; 
      color: white;
      font-weight: bold;
      position: sticky;
      top: 0;
    }}
    .expandable:hover {{ 
      cursor: pointer; 
      background-color: #e8f4f8; 
      transition: background-color 0.2s;
    }}
    .details {{ 
      display: none; 
      background-color: #f8f9fa; 
    }}
    .details ul {{
      margin: 0.5rem 0;
      padding-left: 1.5rem;
    }}
    .details li {{
      margin-bottom: 0.25rem;
    }}
    .rank {{
      font-weight: bold;
      color: #2c3e50;
    }}
    .points {{
      font-weight: bold;
      color: #27ae60;
    }}
    .footer {{ 
      margin-top: 2rem; 
      padding-top: 1rem;
      border-top: 1px solid #eee;
      font-size: 0.9em; 
      color: #666; 
      text-align: center;
    }}
    .stats-row {{
      font-size: 0.9em;
      color: #666;
    }}
    .win-rate {{
      color: #e74c3c;
      font-weight: bold;
    }}
    .top3-rate {{
      color: #f39c12;
      font-weight: bold;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🎱 Skinny Bob's Series - 2025 Season Standings</h1>
    <p class="subtitle">Click on any player row to see their detailed tournament history</p>
    
    <table id="standingsTable">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Player</th>
          <th>Total Points</th>
          <th>Events</th>
          <th>Wins</th>
          <th>Top 3</th>
          <th>Win Rate</th>
          <th>Top 3 Rate</th>
          <th>Last Played</th>
        </tr>
      </thead>
      <tbody id="standingsBody"></tbody>
    </table>
    
    <div class="footer">
      Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
      <small>Data includes {len(standings_data)} players across {len(set(r['tournament'] for r in all_results))} tournaments</small>
    </div>
  </div>

<script>
const standingsData = {standings_json};

// Build the enhanced table
const tbody = document.getElementById('standingsBody');
standingsData.forEach((player, index) => {{
  const rank = index + 1;
  
  // Main row (clickable)
  const tr = document.createElement('tr');
  tr.className = 'expandable';
  
  // Format percentages
  const winRate = player.win_rate ? `${{player.win_rate}}%` : '0%';
  const top3Rate = player.top_3_rate ? `${{player.top_3_rate}}%` : '0%';
  
  tr.innerHTML = `
    <td class="rank">${{rank}}</td>
    <td>${{player.player_name}}</td>
    <td class="points">${{player.total_points || 0}}</td>
    <td>${{player.total_events || 0}}</td>
    <td>${{player.wins || 0}}</td>
    <td>${{player.top_3 || 0}}</td>
    <td class="win-rate">${{winRate}}</td>
    <td class="top3-rate">${{top3Rate}}</td>
    <td>${{player.last_played || 'N/A'}}</td>
  `;
  
  // Details row (hidden by default)
  const details = document.createElement('tr');
  details.className = 'details';
  
  // Build event breakdown
  const eventBreakdown = `
    <strong>Event Breakdown:</strong> 
    Weekly: ${{player.weekly_events || 0}}, 
    Monthly: ${{player.monthly_events || 0}}, 
    Major: ${{player.major_events || 0}}
  `;
  
  // Build tournament history
  const historyHtml = player.history && player.history.length > 0 ? 
    player.history.slice(0, 10).map(function(r) {{
      let place = r.position_orig;
      if (place?.toLowerCase() === "winner") place = "1st";
      const points = r.points !== undefined && r.points !== null ? ` (${{r.points}} pts)` : "";
      const eventType = r.event_type ? ` [${{r.event_type}}]` : "";
      return `<li>${{r.date}} - ${{r.tournament}}: ${{place}}${{points}}${{eventType}}</li>`;
    }}).join('') : '<li>No tournament history available</li>';
  
  const showingNote = player.history && player.history.length > 10 ? 
    `<li><em>Showing most recent 10 of ${{player.history.length}} tournaments</em></li>` : '';
  
  details.innerHTML = `
    <td colspan="9" style="padding: 1rem;">
      <div style="margin-bottom: 1rem;">${{eventBreakdown}}</div>
      <strong>Recent Tournament History:</strong>
      <ul style="margin: 0.5rem 0 0 1.5rem; padding-left: 0; max-height: 300px; overflow-y: auto;">
        ${{historyHtml}}
        ${{showingNote}}
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

// Add some summary stats at the top
console.log(`📊 Loaded standings for ${{standingsData.length}} players`);
console.log(`🏆 Total tournaments: ${{new Set(standingsData.flatMap(p => p.history || []).map(h => h.tournament)).size}}`);
</script>
</body>
</html>"""
        
        # Write the HTML file
        output_file = os.path.join(OFFLINE_HTML_DIR, f"skinny_bobs_improved_standings_{datetime.now().strftime('%Y%m%d')}.html")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Enhanced HTML file generated: {output_file}")
        print(f"📁 This version includes win rates, event breakdowns, and better formatting!")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error generating improved HTML: {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        return None

if __name__ == "__main__":
    export_standings_html_improved()