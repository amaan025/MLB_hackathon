import requests
from datetime import datetime, timedelta

# Base URL for the MLB API
API_BASE_URL = "https://statsapi.mlb.com/api/v1/"

# Fetch the featured game for today
def fetch_featured_game():
    """Fetch the featured game scheduled for today.

    Returns:
        dict: Details of the first game scheduled for today, or None if no games are found.
    """
    today = datetime.utcnow().strftime('%Y-%m-%d')  # Get today's date in UTC
    response = requests.get(f"{API_BASE_URL}schedule", params={
        "sportId": 1,  # Sport ID for MLB
        "date": today,
        "hydrate": "team,venue,probablePitcher",  # Include related details
    })
    response.raise_for_status()  # Raise an error for HTTP issues
    schedule = response.json()  # Parse JSON response
    
    # Extract the first game from today's schedule
    dates = schedule.get('dates', [])
    if dates and dates[0].get('games'):
        return dates[0]['games'][0]
    return None

# Fetch all upcoming games
def fetch_upcoming_games():
    """Fetch a list of upcoming games within the next year.

    Returns:
        list: A list of upcoming games with details.
    """
    start_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')  # Start from tomorrow
    end_date = (datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d')   # End one year from today
    response = requests.get(f"{API_BASE_URL}schedule", params={
        "sportId": 1,
        "startDate": start_date,
        "endDate": end_date,
        "hydrate": "team,venue"  # Include team and venue details
    })
    response.raise_for_status()
    schedule = response.json()  # Parse JSON response

    # Compile all games into a single list
    games = []
    for date in schedule.get('dates', []):
        games.extend(date.get('games', []))
    return games

# Fetch all past games
def fetch_past_games():
    """Fetch a list of past games from the last year.

    Returns:
        list: A list of past games with details, sorted by game date (most recent first).
    """
    end_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')  # End yesterday
    start_date = (datetime.utcnow() - timedelta(days=366)).strftime('%Y-%m-%d')  # Start one year ago
    response = requests.get(f"{API_BASE_URL}schedule", params={
        "sportId": 1,
        "startDate": start_date,
        "endDate": end_date,
        "hydrate": "team,venue"  # Include team and venue details
    })
    response.raise_for_status()
    schedule = response.json()  # Parse JSON response

    # Compile and sort games by date (descending)
    games = []
    for date in schedule.get('dates', []):
        games.extend(date.get('games', []))
    games.sort(key=lambda x: x['gameDate'], reverse=True)
    return games

# Fetch all teams
def fetch_top_teams():
    """Fetch a list of all MLB teams.

    Returns:
        list: A list of teams with their details.
    """
    response = requests.get(f"{API_BASE_URL}teams", params={"sportId": 1})
    response.raise_for_status()  # Raise an error for HTTP issues
    return response.json().get('teams', [])  # Extract team data
