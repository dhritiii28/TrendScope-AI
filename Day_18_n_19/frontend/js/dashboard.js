const token =
    localStorage.getItem("token");

let allTrends = [];


async function loadProfile() {

    const response = await fetch(
        "http://127.0.0.1:8000/profile",
        {
            method: "GET",

            headers: {
                "Authorization":
                    `Bearer ${token}`
            }
        }
    );

    const data =
        await response.json();

    document.getElementById(
        "user-info"
    ).innerText =
        `Logged in as: ${data.user}`;
}

function logout() {

    localStorage.removeItem(
        "token"
    );

    window.location.href =
        "login.html";
}

async function loadTopTrends() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/top_trends"
        );

        const data = await response.json();

        allTrends = data;

        renderTrends(allTrends);

    }

    catch (error) {
        console.log(error);
    }
}

function renderTrends(trends) {

    const container =
        document.getElementById("top-trends");

    container.innerHTML = "";

    trends.forEach(trend => {

        container.innerHTML += `
            <div class="trend-card">

                <h3>${trend.title}</h3>

                <p><strong>Category:</strong> ${trend.category}</p>

                <p><strong>Score:</strong> ${trend.trend_score}</p>

                <p><strong>Source:</strong> ${trend.source}</p>

            </div>
        `;
    });
}

async function searchTrends() {

    const query = document
        .getElementById("searchInput")
        .value;

    if (!query) {
        loadTopTrends();
        return;
    }

    const response = await fetch(
        `http://127.0.0.1:8000/search_trends?query=${query}`
    );

    const data = await response.json();

    renderTrends(data);
}

async function loadPredictions() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/predict_trends"
        );

        const predictions = await response.json();

        const container =
            document.getElementById("predictions");

        container.innerHTML = "";

        predictions.forEach(item => {

            const color =
                item.trend === "Rising"
                ? "#22c55e"
                : "#ef4444";

            const icon =
                item.trend === "Rising"
                ? "📈"
                : "📉";

            container.innerHTML += `

                <div class="trend-card">

                    <h3>${item.topic}</h3>

                    <p>
                        <strong>Category:</strong>
                        ${item.category}
                    </p>

                    <p>
                        Current Score:
                        ${item.current_score.toFixed(1)}
                    </p>

                    <p>
                        Predicted:
                        ${item.predicted_score.toFixed(1)}
                    </p>

                    <p
                        style="
                        color:${color};
                        font-weight:bold;
                        ">

                        ${icon}
                        ${item.trend}

                    </p>

                </div>

            `;

        });

    }

    catch(error){

        console.log(error);

    }

}

async function loadDashboardStats() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/all_trends"
        );

        const trends = await response.json();

        // Total Articles
        document.getElementById("articles").innerText =
            trends.length;

        // Average Trend Score
        const avgScore =
            trends.reduce(
                (sum, item) => sum + item.trend_score,
                0
            ) / trends.length;

        document.getElementById("avg-score").innerText =
            avgScore.toFixed(1);

    }

    catch (error) {

        console.log(error);

    }

}


async function loadTrendChart() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/top_trends?limit=10"
        );

        const trends = await response.json();

        const labels = trends.map(item => {
            return item.title.length > 30
                ? item.title.substring(0, 30) + "..."
                : item.title;
        });

        const scores = trends.map(item => item.trend_score);

        const ctx = document
            .getElementById("trendChart")
            .getContext("2d");

        new Chart(ctx, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [{

                    label: "Trend Score",

                    data: scores,

                    borderWidth: 1

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        labels: {

                            color: "white"

                        }

                    }

                },

                scales: {

                    x: {

                        ticks: {

                            color: "white"

                        }

                    },

                    y: {

                        beginAtZero: true,

                        max: 100,

                        ticks: {

                            color: "white"

                        }

                    }

                }

            }

        });

    }

    catch (error) {

        console.log(error);

    }

}

async function loadCategory(category) {

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/category/${category}`
        );

        const trends = await response.json();

        renderTrends(trends);

    }

    catch (error) {
        console.log(error);
    }
}


loadProfile();
loadDashboardStats();
loadTopTrends();
loadTrendChart();
loadPredictions();