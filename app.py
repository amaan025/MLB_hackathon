from flask import Flask, render_template, jsonify, request
from utils.api_utils import fetch_featured_game, fetch_upcoming_games, fetch_past_games, fetch_top_teams
import requests
from datetime import datetime, timezone

app = Flask(__name__)

# Cache the games data
upcoming_games = fetch_upcoming_games()
past_games = fetch_past_games()

def get_next_game():
    """Get the next upcoming game based on the current datetime."""
    current_time = datetime.now(timezone.utc)  # Make the current time offset-aware
    for game in upcoming_games:
        game_time = datetime.fromisoformat(game['gameDate'].replace("Z", "+00:00"))
        if game_time > current_time:
            return game
    return None

def fetch_player_details(team_name, player_name):
    """Fetch player details using team name and player name."""
    try:
        # Step 1: Get the team ID
        teams = fetch_top_teams()
        team = next((team for team in teams if team['name'].lower() == team_name.lower()), None)
        if not team:
            return {"error": "Team not found"}

        team_id = team['id']

        # Step 2: Get the team roster
        roster_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?season=2025"
        roster_response = requests.get(roster_url)
        roster_response.raise_for_status()
        roster = roster_response.json().get("roster", [])

        # Step 3: Get the player ID
        player = next(
            (player for player in roster if player["person"]["fullName"].lower() == player_name.lower()), None
        )
        if not player:
            return {"error": "Player not found"}

        player_id = player["person"]["id"]

        # Step 4: Get player details
        player_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/"
        player_response = requests.get(player_url)
        player_response.raise_for_status()
        player_details = player_response.json().get("people", [])[0]

        # Step 5: Add headshot URL
        player_details["headshot_url"] = f"https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg"

        return player_details

    except Exception as e:
        return {"error": str(e)}

def fetch_most_followed_players():
    """Fetch and process most followed players data for graph."""
    try:
        url = "https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/mlb-fan-content-interaction-data/2025-mlb-fan-favs-follows.json"
        response = requests.get(url)
        response.raise_for_status()

        # Read JSON lines and count player IDs
        player_counts = {}
        for line in response.text.strip().split("\n"):
            entry = eval(line)  # Parse each JSON object
            for player_id in entry.get("followed_player_ids", []):
                player_counts[player_id] = player_counts.get(player_id, 0) + 1

        # Sort players by followers and fetch top 10
        sorted_players = sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Enrich player data with their names
        enriched_data = []
        for player_id, count in sorted_players:
            player_info = requests.get(f"https://statsapi.mlb.com/api/v1/people/{player_id}").json()
            enriched_data.append({
                "player_name": player_info["people"][0]["fullName"],
                "followers": count
            })

        return enriched_data

    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    try:
        featured_game = fetch_featured_game()
        next_game = get_next_game()
        return render_template(
            'home.html',
            featured_game=featured_game,
            next_game=next_game,  # Pass next game for countdown
            upcoming_games=upcoming_games[:10],  # Display the first 10 upcoming games
            past_games=past_games[:10],  # Display the first 10 past games
            top_teams=fetch_top_teams()  # Fetch all top teams
        )
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/api/upcoming-games')
def api_upcoming_games():
    """API endpoint to provide paginated upcoming games."""
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('limit', 10))
    return jsonify(upcoming_games[start:start + limit])

@app.route('/api/past-games')
def api_past_games():
    """API endpoint to provide paginated past games."""
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('limit', 10))
    return jsonify(past_games[start:start + limit])

@app.route('/teams')
def teams():
    try:
        # Fetch all teams
        teams_data = fetch_top_teams()
        
        # Extract relevant data
        teams = [
            {
                "team": team['name'],
                "locationName": team['locationName'],
                "league_name": team['league']['name'],
                "division_name": team['division']['name']
            }
            for team in teams_data
        ]
        
        return render_template('teams.html', teams=teams)
    except Exception as e:
        return f"An error occurred while fetching teams: {e}"

@app.route('/players', methods=['GET', 'POST'])
def players():
    player_details = None
    error = None
    top_followed_players = fetch_most_followed_players()

    if request.method == 'POST':
        team_name = request.form.get('team_name')
        player_name = request.form.get('player_name')

        if team_name and player_name:
            result = fetch_player_details(team_name, player_name)
            if "error" in result:
                error = result["error"]
            else:
                player_details = result
        else:
            error = "Please provide both team name and player name."

    return render_template(
        'players.html',
        player_details=player_details,
        error=error,
        top_followed_players=top_followed_players
    )

@app.route('/api/top-followed-players')
def api_top_followed_players():
    """API endpoint for the top followed players."""
    return jsonify(fetch_most_followed_players())

if __name__ == '__main__':
    app.run(debug=True)
