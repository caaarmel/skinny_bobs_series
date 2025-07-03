import sqlite3
import json
import os
from datetime import datetime
from config import DB_PATH, OFFLINE_HTML_DIR

def export_multi_page_standings():
    """
    Generate HTML export with clickable tournament links that show full tournament results
    """
    
    # Ensure output directory exists
    os.makedirs(OFFLINE_HTML_DIR, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    print("🏆 Generating multi-page standings HTML with tournament links...")
    
    try:
        # Use your season_2025_standings view for the main standings
        standings_query = """
        SELECT 
            Player as player_name,
            total_pts as total_points,
            total_events,
            Wins as wins,
            top_3,
            top_8,
            weekly_events,
            monthly_events,
            major_events,
            win_rate_pct as win_rate,
            top_3_pct as top_3_rate,
            last_played
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
            points,
            UPPER(SUBSTR(event_type_name, 1, 1)) || LOWER(SUBSTR(event_type_name, 2)) AS event_type,
            pt_structure,
            event_id,
            total_players
        FROM results_public
        ORDER BY date DESC, position_std ASC
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
        
        # Group results by tournament for tournament pages
        tournament_results = {}
        tournaments_list = []
        for result in all_results:
            tournament_key = f"{result['tournament']}_{result['date']}"
            tournament_name = result['tournament']
            tournament_date = result['date']
            
            if tournament_key not in tournament_results:
                tournament_results[tournament_key] = {
                    'name': tournament_name,
                    'date': tournament_date,
                    'event_type': result['event_type'],
                    'total_players': result['total_players'],
                    'pt_structure': result['pt_structure'],
                    'results': []
                }
                tournaments_list.append({
                    'key': tournament_key,
                    'name': tournament_name,
                    'date': tournament_date,
                    'event_type': result['event_type'],
                    'pt_structure': result['pt_structure']
                })
            
            tournament_results[tournament_key]['results'].append(result)
        
        # Sort tournaments by date (most recent first)
        tournaments_list.sort(key=lambda x: x['date'], reverse=True)
        
        # Combine standings with history
        for player_data in standings_data:
            player_name = player_data['player_name']
            player_data['history'] = player_history.get(player_name, [])
        
        # Convert to JSON for embedding
        standings_json = json.dumps(standings_data, indent=0, separators=(',', ': '))
        tournaments_json = json.dumps(tournament_results, indent=0, separators=(',', ': '))
        tournaments_list_json = json.dumps(tournaments_list, indent=0, separators=(',', ': '))
        
        # Generate the main HTML with navigation
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Skinny Bob's 2025 Season Standings</title>
  <style>
    body {{ 
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
      margin: 0; 
      background-color: #f8f9fa;
    }}
    .navbar {{
      background-color: #2c3e50;
      padding: 1rem 2rem;
      color: white;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .navbar h1 {{
      margin: 0;
      font-size: 1.5rem;
    }}
    .nav-buttons {{
      margin-top: 0.5rem;
    }}
    .nav-btn {{
      background-color: #34495e;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      margin-right: 0.5rem;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.2s;
    }}
    .nav-btn:hover {{
      background-color: #4a6741;
    }}
    .nav-btn.active {{
      background-color: #27ae60;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background-color: white;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      margin-top: 2rem;
      margin-bottom: 2rem;
    }}
    .page {{
      display: none;
    }}
    .page.active {{
      display: block;
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
      top: 80px;
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
    .tournament-link {{
      color: #3498db;
      text-decoration: underline;
      cursor: pointer;
    }}
    .tournament-link:hover {{
      color: #2980b9;
    }}
    .rank {{
      font-weight: bold;
      color: #2c3e50;
    }}
    .points {{
      font-weight: bold;
      color: #27ae60;
    }}
    .position-1 {{ color: #f1c40f; font-weight: bold; }}
    .position-2 {{ color: #95a5a6; font-weight: bold; }}
    .position-3 {{ color: #e67e22; font-weight: bold; }}
    .footer {{ 
      margin-top: 2rem; 
      padding-top: 1rem;
      border-top: 1px solid #eee;
      font-size: 0.9em; 
      color: #666; 
      text-align: center;
    }}
    .tournament-header {{
      background-color: #ecf0f1;
      padding: 1rem;
      border-radius: 4px;
      margin-bottom: 1rem;
    }}
    .tournament-list {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }}
    .tournament-card {{
      border: 1px solid #ddd;
      border-radius: 6px;
      padding: 1rem;
      background-color: #fff;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .tournament-card:hover {{
      border-color: #3498db;
      box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
    }}
    .tournament-card h4 {{
      margin: 0 0 0.5rem 0;
      color: #2c3e50;
    }}
    .tournament-card .meta {{
      color: #7f8c8d;
      font-size: 0.9em;
    }}
  </style>
</head>
<body>
  <div class="navbar">
    <h1>Skinny Bob's Series - 2025 Season</h1>
    <div class="nav-buttons">
      <button class="nav-btn active" onclick="showPage('standings')">Player Standings</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Tournament Results</button>
      <button class="nav-btn" onclick="showPage('tournament-list')">All Tournaments</button>
    </div>
  </div>

  <div class="container">
    <!-- Player Standings Page -->
    <div id="standings" class="page active">
      <h2>Player Standings</h2>
      <p>Click on any player row to see their detailed tournament history. Tournament names are clickable links.</p>
      
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
    </div>

    <!-- Tournament Results Page -->
    <div id="tournaments" class="page">
      <div id="tournamentContent">
        <h2>Select a Tournament</h2>
        <p>Use the navigation above or click a tournament link from a player's history.</p>
      </div>
    </div>

    <!-- Tournament List Page -->
    <div id="tournament-list" class="page">
      <h2>All Tournaments</h2>
      <div id="tournamentListContent"></div>
    </div>

    <div class="footer">
      Last Updated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
      <small>{len(standings_data)} players across {len(tournaments_list)} tournaments</small>
    </div>
  </div>

<script>
const standingsData = {standings_json};
const tournamentResults = {tournaments_json};
const tournamentsList = {tournaments_list_json};

// Navigation functions
function showPage(pageId) {{
  // Hide all pages
  document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
  
  // Show selected page
  document.getElementById(pageId).classList.add('active');
  event.target.classList.add('active');
}}

function showTournament(tournamentKey) {{
  const tournament = tournamentResults[tournamentKey];
  if (!tournament) return;
  
  // Switch to tournaments page
  showPage('tournaments');
  document.querySelector('[onclick="showPage(\\'tournaments\\')"]').classList.add('active');
  
  // Sort results by position
  const sortedResults = tournament.results.sort((a, b) => {{
    if (a.position_std === null) return 1;
    if (b.position_std === null) return -1;
    return a.position_std - b.position_std;
  }});
  
  const tournamentHtml = `
    <div class="tournament-header">
      <h2>${{tournament.name}}</h2>
      <p><strong>Date:</strong> ${{tournament.date}} |  <strong>Players:</strong> ${{tournament.total_players}} |  <strong>Type:</strong> ${{toProperCase(tournament.event_type)}} - ${{tournament.pt_structure}}</p>
    </div>
    
    <table>
      <thead>
        <tr>
          <th>Position</th>
          <th>Player</th>
          <th>Points</th>
        </tr>
      </thead>
      <tbody>
        ${{sortedResults.map(r => {{
          let positionClass = '';
          if (r.position_std === 1) positionClass = 'position-1';
          else if (r.position_std === 2) positionClass = 'position-2';
          else if (r.position_std === 3) positionClass = 'position-3';
          
          let position = r.position_orig;
          if (position?.toLowerCase() === 'winner') position = '1st';
          
          return `<tr>
            <td class="${{positionClass}}">${{position}}</td>
            <td>${{r.player_name}}</td>
            <td class="points">${{r.points || 0}}</td>
          </tr>`;
        }}).join('')}}
      </tbody>
    </table>
  `;
  
  document.getElementById('tournamentContent').innerHTML = tournamentHtml;
}}

// Helper function to convert text to proper case
function toProperCase(str) {{
  if (!str) return '';
  
  // Words that should stay lowercase in proper case
  const smallWords = ['a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'is', 'of', 'on', 'or', 'the', 'to', 'up', 'via', 'vs'];
  
  return str.toLowerCase().replace(/\w+/g, (word, index) => {{
    // Always capitalize the first word
    if (index === 0) {{
      return word.charAt(0).toUpperCase() + word.slice(1);
    }}
    
    // Keep small words lowercase unless they're the first word
    if (smallWords.includes(word.toLowerCase())) {{
      return word.toLowerCase();
    }}
    
    // Capitalize other words
    return word.charAt(0).toUpperCase() + word.slice(1);
  }});
}}

// Build tournament list page
function buildTournamentList() {{
  const tournamentCards = tournamentsList.map(t => {{
    const tournamentKey = t.key;
    const tournament = tournamentResults[tournamentKey];
    return `
      <div class="tournament-card" onclick="showTournament('${{tournamentKey}}')">
        <h4>${{t.name}}</h4>
        <div class="meta">
          ${{t.date}} ▪ ${{toProperCase(t.event_type)}} ▪ ${{tournament.total_players}} players
        </div>
      </div>
    `;
  }}).join('');
  
  document.getElementById('tournamentListContent').innerHTML = `
    <div class="tournament-list">
      ${{tournamentCards}}
    </div>
  `;
}}

// Build the standings table
function buildStandingsTable() {{
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
      <td>${{winRate}}</td>
      <td>${{top3Rate}}</td>
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
    
    // Build tournament history with clickable links
    const historyHtml = player.history && player.history.length > 0 ? 
      player.history.map(function(r) {{
        let place = `${{r.position_orig}} place`;
        if (place?.toLowerCase() === "winner") place = "1st place";
        const eventType = r.event_type ? ` ▪ ${{toProperCase(r.event_type)}}: ` : "";
        const points = r.points !== undefined && r.points !== null ? `: ${{r.points}} pts` : "";
        const tournamentKey = `${{r.tournament}}_${{r.date}}`;
        
        return `<li>${{r.date}} - <span class="tournament-link" onclick="showTournament('${{tournamentKey}}')">${{r.tournament}}</span>: ${{place}}${{eventType ? ` ▪ ${{toProperCase(r.event_type)}}${{points}}` : ''}}</li>`;
      }}).join('') : '<li>No tournament history available</li>';
    
    const showingNote = player.history && player.history.length > 0 ? 
      `<li><em>Showing all ${{player.history.length}} tournaments</em></li>` : '';
    
    details.innerHTML = `
      <td colspan="9" style="padding: 1rem;">
        <div style="margin-bottom: 1rem;">${{eventBreakdown}}</div>
        <strong>Tournament History:</strong>
        <ul style="margin: 0.5rem 0 0 1.5rem; padding-left: 0; max-height: 400px; overflow-y: auto;">
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
}}

// Initialize the page
buildStandingsTable();
buildTournamentList();

console.log(`📊 Loaded standings for ${{standingsData.length}} players`);
console.log(`🏆 Available tournaments: ${{Object.keys(tournamentResults).length}}`);
</script>
</body>
</html>"""
        
        # Write the HTML file
        output_file = os.path.join(OFFLINE_HTML_DIR, f"skinny_bobs_multi_page_{datetime.now().strftime('%Y%m%d')}.html")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Multi-page HTML file generated: {output_file}")
        print(f"📁 Features:")
        print(f"   - Player standings with clickable tournament links")
        print(f"   - Individual tournament result pages")
        print(f"   - Tournament list browser")
        print(f"   - Navigation between all views")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error generating multi-page HTML: {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        return None

if __name__ == "__main__":
    export_multi_page_standings()