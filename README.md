# MLB Fan Hub

**MLB Fan Hub** is a Flask-based web application that provides fans of Major League Baseball (MLB) with comprehensive information about teams, players, and game schedules. The application is designed to deliver dynamic content using APIs, interactive features, and a user-friendly interface.

---

## Features

### Core Functionality:
- **Home Page**:
  - Displays the featured game of the day.
  - Provides a countdown to the next scheduled game.
  - Lists upcoming and past games with pagination.
- **Teams Page**:
  - Lists MLB teams with details such as team name, location, league, and division.
- **Players Page**:
  - Allows users to search for player details based on team and player name.
  - Displays comprehensive player information, including headshot, position, age, birthplace, height, weight, and MLB debut date.

### Interactive Features:
- Countdown timer for the next game.
- “Load More” functionality for viewing additional upcoming and past games.

---

## Project Structure

```
mlb_fan_coach/
│
├── app.py                # Main Flask app handling routes and logic
├── templates/            # HTML templates for rendering web pages
│   ├── home.html         # Home page layout
│   ├── teams.html        # Teams information page
│   ├── players.html      # Player search page
│
├── static/               # Static files
│   ├── css/              # CSS styling folder
│   │   └── style.css     # Main CSS file
│   ├── script.js         # JavaScript for interactivity
│
├── utils/                # Utility functions
│   └── api_utils.py      # Functions to interact with MLB APIs
│
└── requirements.txt      # Python dependencies
```

---

## Setup and Installation

### Prerequisites
1. **Python 3.9 or above**
2. **pip (Python Package Installer)**

### Steps to Run the Application Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mlb-fan-hub.git
   cd mlb-fan-hub
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python app.py
   ```

5. **Open the application in your browser**:
   - Navigate to `http://127.0.0.1:5000`.

---

## API Endpoints

### Public Endpoints:
- **`/api/upcoming-games`**:
  - Fetches upcoming games with pagination.
  - Query Parameters:
    - `start`: Starting index (default: 0).
    - `limit`: Number of games to fetch (default: 10).
- **`/api/past-games`**:
  - Fetches past games with pagination.
  - Query Parameters:
    - `start`: Starting index (default: 0).
    - `limit`: Number of games to fetch (default: 10).

---

## Technologies Used
- **Back-End**: Flask, Python
- **Front-End**: HTML, CSS, JavaScript (Vanilla)
- **APIs**: MLB Stats API
- **Version Control**: Git, GitHub
- **Containerization**: Docker (Optional)

---

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact
- **Author**: Amaan Ahmad
- **Email**: ahmadamaan082@gmail.com
- **GitHub**: [amaan025](https://github.com/amaan025)
