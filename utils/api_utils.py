import requests
from datetime import datetime, timedelta

API_BASE_URL = "https://statsapi.mlb.com/api/v1/"

# Fetch game for today
def fetch_featured_game():
    today = datetime.utcnow().strftime('%Y-%m-%d')
    response = requests.get(f"{API_BASE_URL}schedule", params={
        "sportId": 1,
        "date": today,
        "hydrate": "team,venue,probablePitcher",
    })
    response.raise_for_status()
    schedule = response.json()
    dates = schedule.get('dates', [])
    if dates and dates[0].get('games'):
        return dates[0]['games'][0]
    return None

# Fetch upcoming games
def fetch_upcoming_games():
    start_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d')
    response = requests.get(f"{API_BASE_URL}schedule", params={
        "sportId": 1,
        "startDate": start_date,
        "endDate": end_date,
        "hydrate": "team,venue"
    })
    response.raise_for_status()
    schedule = response.json()
    games = []
    for date in schedule.get('dates', []):
        games.extend(date.get('games', []))
    return games

# Fetch past games
def fetch_past_games():
    end_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.utcnow() - timedelta(days=366)).strftime('%Y-%m-%d')
    response = requests.get(f"{API_BASE_URL}schedule", params={
        "sportId": 1,
        "startDate": start_date,
        "endDate": end_date,
        "hydrate": "team,venue"
    })
    response.raise_for_status()
    schedule = response.json()
    games = []
    for date in schedule.get('dates', []):
        games.extend(date.get('games', []))
    games.sort(key=lambda x: x['gameDate'], reverse=True)
    return games

# Fetch teams from the API
def fetch_top_teams():
    response = requests.get(f"{API_BASE_URL}teams", params={"sportId": 1})
    response.raise_for_status()
    return response.json().get('teams', [])
