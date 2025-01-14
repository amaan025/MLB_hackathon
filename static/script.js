document.addEventListener("DOMContentLoaded", () => {
    // Countdown Timer for the Next Game
    const countdownElement = document.getElementById('countdown-timer');
    const nextGameTime = countdownElement?.getAttribute('data-game-time');

    if (countdownElement && nextGameTime) {
        const targetDate = new Date(nextGameTime);

        // Update the countdown timer every second
        function updateCountdown() {
            const now = new Date();
            const diff = targetDate - now;

            // If the countdown reaches zero
            if (diff <= 0) {
                countdownElement.textContent = "The next game is starting now!";
                clearInterval(interval); // Stop the timer
                return;
            }

            // Calculate days, hours, minutes, and seconds
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((diff / (1000 * 60)) % 60);
            const seconds = Math.floor((diff / 1000) % 60);

            // Update the countdown element
            countdownElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }

        updateCountdown(); // Initialize countdown immediately
        const interval = setInterval(updateCountdown, 1000); // Update every second
    }

    // Load More Buttons for Upcoming and Past Games
    const loadMoreUpcoming = document.getElementById('load-more-upcoming');
    const loadMorePast = document.getElementById('load-more-past');

    const upcomingGamesTable = document.getElementById('upcoming-games-table');
    const pastGamesTable = document.getElementById('past-games-table');

    let upcomingDisplayed = 10; // Number of upcoming games currently displayed
    let pastDisplayed = 10; // Number of past games currently displayed

    // Load more upcoming games
    loadMoreUpcoming?.addEventListener('click', () => {
        fetch(`/api/upcoming-games?start=${upcomingDisplayed}&limit=10`)
            .then(response => response.json())
            .then(newGames => {
                // Append new games to the upcoming games table
                newGames.forEach(game => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${game.teams.home.team.name} vs ${game.teams.away.team.name}</td>
                        <td>${game.gameDate}</td>
                        <td>${game.venue.name}</td>
                    `;
                    upcomingGamesTable.appendChild(row);
                });
                upcomingDisplayed += newGames.length;

                // Hide the button if no more games are available
                if (newGames.length < 10) {
                    loadMoreUpcoming.style.display = 'none';
                }
            });
    });

    // Load more past games
    loadMorePast?.addEventListener('click', () => {
        fetch(`/api/past-games?start=${pastDisplayed}&limit=10`)
            .then(response => response.json())
            .then(newGames => {
                // Append new games to the past games table
                newGames.forEach(game => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${game.teams.home.team.name} vs ${game.teams.away.team.name}</td>
                        <td>${game.gameDate}</td>
                        <td>${game.venue.name}</td>
                    `;
                    pastGamesTable.appendChild(row);
                });
                pastDisplayed += newGames.length;

                // Hide the button if no more games are available
                if (newGames.length < 10) {
                    loadMorePast.style.display = 'none';
                }
            });
    });
});
