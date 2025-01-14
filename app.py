from flask import Flask, render_template, jsonify, request
from utils.api_utils import fetch_featured_game, fetch_upcoming_games, fetch_past_games, fetch_top_teams
import requests
from datetime import datetime, timezone

# Initialize Flask application
app = Flask(__name__)

# Pre-fetch games data for caching and performance
upcoming_games = fetch_upcoming_games()  # List of upcoming games
past_games = fetch_past_games()          # List of past games

def get_next_game():
    """Retrieve the next upcoming game based on the current UTC time."""
    current_time = datetime.now(timezone.utc)  # Get current time in UTC
    for game in upcoming_games:
        # Convert game date to a timezone-aware datetime object
        game_time = datetime.fromisoformat(game['gameDate'].replace("Z", "+00:00"))
        if game_time > current_time:
            return game  # Return the next game
    return None  # No upcoming game found

def fetch_player_details(team_name, player_name):
    """Fetch details of a player using the team name and player name."""
    try:
        # Step 1: Retrieve team information
        teams = fetch_top_teams()
        team = next((team for team in teams if team['name'].lower() == team_name.lower()), None)
        if not team:
            return {"error": "Team not found"}

        team_id = team['id']  # Extract team ID

        # Step 2: Fetch team roster
        roster_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?season=2025"
        roster_response = requests.get(roster_url)
        roster_response.raise_for_status()
        roster = roster_response.json().get("roster", [])

        # Step 3: Find the player in the roster
        player = next(
            (player for player in roster if player["person"]["fullName"].lower() == player_name.lower()), None
        )
        if not player:
            return {"error": "Player not found"}

        player_id = player["person"]["id"]  # Extract player ID

        # Step 4: Retrieve player details
        player_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/"
        player_response = requests.get(player_url)
        player_response.raise_for_status()
        player_details = player_response.json().get("people", [])[0]

        # Step 5: Add headshot URL to player details
        player_details["headshot_url"] = f"https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg"

        return player_details

    except Exception as e:
        return {"error": str(e)}  # Return error details

@app.route('/')
def home():
    """Render the home page with featured game, next game, and games lists."""
    try:
        featured_game = fetch_featured_game()  # Featured game details
        next_game = get_next_game()           # Next upcoming game
        return render_template(
            'home.html',
            featured_game=featured_game,
            next_game=next_game,                # Pass next game details for countdown
            upcoming_games=upcoming_games[:10], # First 10 upcoming games
            past_games=past_games[:10],         # First 10 past games
            top_teams=fetch_top_teams()         # List of top teams
        )
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/api/upcoming-games')
def api_upcoming_games():
    """API endpoint to retrieve paginated upcoming games."""
    start = int(request.args.get('start', 0))  # Start index (default: 0)
    limit = int(request.args.get('limit', 10)) # Number of games to fetch (default: 10)
    return jsonify(upcoming_games[start:start + limit])

@app.route('/api/past-games')
def api_past_games():
    """API endpoint to retrieve paginated past games."""
    start = int(request.args.get('start', 0))  # Start index (default: 0)
    limit = int(request.args.get('limit', 10)) # Number of games to fetch (default: 10)
    return jsonify(past_games[start:start + limit])

@app.route('/teams')
def teams():
    """Render the teams page with a list of top teams and their details."""
    try:
        teams_data = fetch_top_teams()  # Fetch top teams data

        # Extract and format relevant team information
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
    """Render the players page and handle player details lookup."""
    player_details = None
    error = None

    if request.method == 'POST':
        # Retrieve form data
        team_name = request.form.get('team_name')
        player_name = request.form.get('player_name')

        if team_name and player_name:
            # Fetch player details
            result = fetch_player_details(team_name, player_name)
            if "error" in result:
                error = result["error"]  # Set error message
            else:
                player_details = result  # Set player details
        else:
            error = "Please provide both team name and player name."

    return render_template('players.html', player_details=player_details, error=error)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
