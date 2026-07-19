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

    const container = document.getElementById("top-trends");

    container.innerHTML = "";

    if (trends.length === 0) {

        container.innerHTML = `
            <div class="no-results">
                <i class="fa-solid fa-magnifying-glass"></i>
                <h3>No trends found</h3>
                <p>Try searching for another keyword.</p>
            </div>
        `;

        return;
    }

    trends.forEach(trend => {

        container.innerHTML += `

            <div class="trend-card">

                <div class="trend-header">

                    <span class="category-badge">
                        ${trend.category}
                    </span>

                    <span class="score-badge">
                        ⭐ ${trend.trend_score}
                    </span>

                </div>

                <h3>${trend.title}</h3>

                <p class="source">
                    <i class="fa-solid fa-globe"></i>
                    ${trend.source}
                </p>

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

        // ----------------------------
        // Average Prediction
        // ----------------------------

        const avgPrediction =
            predictions.reduce(
                (sum, item) => sum + item.predicted_score,
                0
            ) / predictions.length;

        document.getElementById(
            "predictionAverage"
        ).innerText =
            avgPrediction.toFixed(1);

        // ----------------------------
        // Prediction Cards
        // ----------------------------

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

            <div class="prediction-card">

                <div class="prediction-header">

                    <span class="prediction-category">
                        ${item.category}
                    </span>

                    <span
                        class="prediction-status"
                        style="color:${color};">

                        ${icon} ${item.trend}

                    </span>

                </div>

                <h3>${item.topic}</h3>

                <div class="prediction-values">

                    <div>

                        <small>Current Score</small>

                        <h4>${Math.round(item.current_score)}</h4>

                    </div>

                    <div>

                        <small>Predicted Score</small>

                        <h4>${Math.round(item.predicted_score)}</h4>

                    </div>

                </div>

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
            "http://127.0.0.1:8000/category_stats"
        );

        const data = await response.json();

        // Sort categories by average score (highest first)
        data.sort((a, b) => b.avg_score - a.avg_score);

        const labels = data.map(item => item.category);

        const scores = data.map(item => item.avg_score);

        const ctx = document
            .getElementById("trendChart")
            .getContext("2d");

        new Chart(ctx, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [{

                    label: "Average Trend Score",

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

document.querySelectorAll(".category-filter button").forEach(button => {

    button.addEventListener("click", () => {

        document
            .querySelectorAll(".category-filter button")
            .forEach(btn => btn.classList.remove("active"));

        button.classList.add("active");

    });

});

async function loadCategories(){

    const response = await fetch(
        "http://127.0.0.1:8000/domains"
    );

    const data = await response.json();

    const select1 = document.getElementById("category1");
    const select2 = document.getElementById("category2");

    data.domains.forEach(category=>{

        select1.innerHTML +=
        `<option value="${category}">
            ${category}
        </option>`;

        select2.innerHTML +=
        `<option value="${category}">
            ${category}
        </option>`;

    });

}

let comparisonChart = null;

async function compareCategories() {

    const cat1 = document.getElementById("category1").value;
    const cat2 = document.getElementById("category2").value;

    if (!cat1 || !cat2) {

        alert("Please select both categories.");

        return;

    }

    if (cat1 === cat2) {

        alert("Please choose two different categories.");

        return;

    }

    const response = await fetch(
        `http://127.0.0.1:8000/compare_categories?cat1=${cat1}&cat2=${cat2}`
    );

    const data = await response.json();

    const category1 = data[cat1];
    const category2 = data[cat2];

    renderComparisonCards(category1, category2);

    drawComparisonChart(category1, category2);

    generateComparisonSummary(category1, category2);

}

function renderComparisonCards(cat1, cat2) {

    const container =
        document.getElementById("comparison-results");

    container.innerHTML = `

        <div class="compare-card">

            <h3>📂 ${cat1.category.toUpperCase()}</h3>

            <p><strong>📰 Articles:</strong> ${cat1.articles}</p>

            <p><strong>⭐ Average Score:</strong> ${cat1.avg_score}</p>

            <p><strong>🤖 Predicted Score:</strong> ${cat1.predicted_score}</p>

            <p><strong>📈 Growth:</strong> +${cat1.growth}</p>

        </div>

        <div class="compare-card">

            <h3>📂 ${cat2.category.toUpperCase()}</h3>

            <p><strong>📰 Articles:</strong> ${cat2.articles}</p>

            <p><strong>⭐ Average Score:</strong> ${cat2.avg_score}</p>

            <p><strong>🤖 Predicted Score:</strong> ${cat2.predicted_score}</p>

            <p><strong>📈 Growth:</strong> +${cat2.growth}</p>

        </div>

    `;

}

function drawComparisonChart(cat1, cat2) {

    const ctx = document
        .getElementById("comparisonChart")
        .getContext("2d");

    if (comparisonChart) {
        comparisonChart.destroy();
    }

    comparisonChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [

                "Articles",
                "Average Score",
                "Predicted Score",
                "Growth"

            ],

            datasets: [

                {

                    label: cat1.category,

                    data: [

                        cat1.articles,
                        cat1.avg_score,
                        cat1.predicted_score,
                        cat1.growth

                    ],

                    borderRadius: 8

                },

                {

                    label: cat2.category,

                    data: [

                        cat2.articles,
                        cat2.avg_score,
                        cat2.predicted_score,
                        cat2.growth

                    ],

                    borderRadius: 8

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "top",

                    labels: {

                        color: "white"

                    }

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "white"

                    },

                    grid: {

                        color: "rgba(255,255,255,.08)"

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        color: "white"

                    },

                    grid: {

                        color: "rgba(255,255,255,.08)"

                    }

                }

            }

        }

    });

}

function generateComparisonSummary(cat1, cat2){

    const winner =
        cat1.predicted_score > cat2.predicted_score
        ? cat1
        : cat2;

    const loser =
        winner.category === cat1.category
        ? cat2
        : cat1;

    document.getElementById("comparison-summary").innerHTML = `

        <h3>AI Category Insight</h3>

        <p>

        <strong>${winner.category.toUpperCase()}</strong>
        is expected to outperform
        <strong>${loser.category.toUpperCase()}</strong>
        based on current trend analysis.

        </p>

        <br>

        <table class="summary-table">

            <tr>

                <td>Winning Category</td>

                <td><strong>${winner.category}</strong></td>

            </tr>

            <tr>

                <td>Predicted Score</td>

                <td>${winner.predicted_score}</td>

            </tr>

            <tr>

                <td>Growth</td>

                <td>+${winner.growth}%</td>

            </tr>

        </table>

    `;

}

async function loadAnalyticsDashboard() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/category_stats"
        );

        const data = await response.json();

        // Sort by average score
        data.sort((a, b) => b.avg_score - a.avg_score);

        // ----------------------------
        // KPI Cards
        // ----------------------------

        const totalArticles = data.reduce(
            (sum, item) => sum + item.articles,
            0
        );

        const averageScore =
            data.reduce(
                (sum, item) => sum + item.avg_score,
                0
            ) / data.length;

        document.getElementById("analyticsArticles").innerText =
            totalArticles;

        document.getElementById("analyticsAverage").innerText =
            averageScore.toFixed(1);

        document.getElementById("topCategory").innerText =
            data[0].category.toUpperCase();

        // Prediction card will be updated later
        document.getElementById("predictionAverage").innerText =
            "--";



        // ----------------------------
        // Doughnut Chart
        // ----------------------------

        new Chart(

            document.getElementById("categoryDistributionChart"),

            {

                type: "doughnut",

                data: {

                    labels: data.map(item => item.category),

                    datasets: [{

                        data: data.map(item => item.articles)

                    }]

                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {

                            position: "bottom",

                            labels: {

                                color: "white"

                            }

                        }

                    }

                }

            }

        );



        // ----------------------------
        // Horizontal Bar Chart
        // ----------------------------

        new Chart(

            document.getElementById("topCategoriesChart"),

            {

                type: "bar",

                data: {

                    labels: data.map(item => item.category),

                    datasets: [{

                        label: "Average Trend Score",

                        data: data.map(item => item.avg_score)

                    }]

                },

                options: {

                    indexAxis: "y",

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

                            beginAtZero: true,

                            max: 100,

                            ticks: {

                                color: "white"

                            }

                        },

                        y: {

                            ticks: {

                                color: "white"

                            }

                        }

                    }

                }

            }

        );

    }

    catch (error) {

        console.log(error);

    }

}

async function loadCategoryInsights(){

    const response = await fetch(
        "http://127.0.0.1:8000/category_stats"
    );

    const data = await response.json();

    data.sort((a,b)=>b.avg_score-a.avg_score);

    const container =
        document.getElementById("categoryInsights");

    container.innerHTML="";

    data.forEach((item,index)=>{

        let performance="Average";

        if(item.avg_score>=80)
            performance="Excellent";

        else if(item.avg_score>=70)
            performance="Good";

        container.innerHTML +=`

        <div class="insight-card">

            <h3>${item.category.toUpperCase()}</h3>

            <p><strong>Articles:</strong> ${item.articles}</p>

            <p><strong>Average Score:</strong> ${item.avg_score}</p>

            <p><strong>Rank:</strong> #${index+1}</p>

            <span class="performance">

                ${performance}

            </span>

        </div>

        `;

    });

}


loadProfile();
loadDashboardStats();
loadTopTrends();
loadPredictions();
loadCategories();
loadAnalyticsDashboard();
loadCategoryInsights();