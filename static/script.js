document.addEventListener("DOMContentLoaded", () => {
    // Countdown Timer for the Next Game
    const countdownElement = document.getElementById('countdown-timer');
    const nextGameTime = countdownElement?.getAttribute('data-game-time');

    if (countdownElement && nextGameTime) {
        const targetDate = new Date(nextGameTime);

        function updateCountdown() {
            const now = new Date();
            const diff = targetDate - now;

            if (diff <= 0) {
                countdownElement.textContent = "The next game is starting now!";
                clearInterval(interval);
                return;
            }

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((diff / (1000 * 60)) % 60);
            const seconds = Math.floor((diff / 1000) % 60);

            countdownElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }

        updateCountdown();
        const interval = setInterval(updateCountdown, 1000);
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

                if (newGames.length < 10) {
                    loadMorePast.style.display = 'none';
                }
            });
    });
});



document.addEventListener("DOMContentLoaded", () => {
    // Fetch the graph data
    fetch("/api/most-followed-players")
        .then((response) => response.json())
        .then((data) => {
            const playerNames = data.map((item) => item.name);
            const playerCounts = data.map((item) => item.count);

            // Create the chart
            const ctx = document.getElementById("most-followed-players-chart").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: playerNames,
                    datasets: [
                        {
                            label: "Number of Followers",
                            data: playerCounts,
                            backgroundColor: "rgba(0, 82, 155, 0.8)",
                            borderColor: "rgba(0, 41, 77, 1)",
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `${context.raw} Followers`;
                                },
                            },
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return value.toLocaleString(); // Format numbers
                                },
                            },
                        },
                    },
                },
            });
        });
});
