// ======================================================
// Dashboard.js
// Part 1
// Authentication + UI + Trends
// ======================================================

const token = localStorage.getItem("token");

let allTrends = [];

// Prevent duplicate chart creation
let trendChart = null;
let comparisonChart = null;
let categoryChart = null;
let topCategoryChart = null;


// ======================================================
// Toast Notification
// ======================================================

function showToast(message, type = "success") {

    const toast = document.getElementById("toast");
    const text = document.getElementById("toastMessage");
    const icon = document.getElementById("toastIcon");

    toast.className = "toast";
    toast.classList.add(type);

    text.innerText = message;

    switch(type){

        case "success":
            icon.className =
                "fa-solid fa-circle-check";
            break;

        case "error":
            icon.className =
                "fa-solid fa-circle-xmark";
            break;

        default:
            icon.className =
                "fa-solid fa-triangle-exclamation";

    }

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    },3000);

}



// ======================================================
// Loader
// ======================================================

function showLoader(){

    document
        .getElementById("loader")
        .classList.remove("loader-hidden");

}

function hideLoader(){

    document
        .getElementById("loader")
        .classList.add("loader-hidden");

}



// ======================================================
// Profile
// ======================================================

async function loadProfile(){

    try{

        const data = await apiRequest(

            "/profile",

            {

                method:"GET",

                headers:{
                    Authorization:`Bearer ${token}`
                }

            }

        );

        document.getElementById("user-info").innerText =
            `Logged in as: ${data.user}`;

    }

    catch(error){

        console.error(error);

        showToast(
            "Unable to load profile.",
            "error"
        );

    }

}



// ======================================================
// Logout
// ======================================================

function handleLogout(){

    showToast(
        "Logged out successfully",
        "success"
    );

    setTimeout(logout,800);

}

function logout(){

    localStorage.removeItem("token");

    window.location.href =
        "login.html";

}



// ======================================================
// Top Trends
// ======================================================

async function loadTopTrends(){

    try{

        const data =
            await apiRequest("/top_trends");

        allTrends = data;

        renderTrends(allTrends);

    }

    catch(error){

        console.error(error);

        showToast(
            "Unable to load top trends.",
            "error"
        );

    }

}



// ======================================================
// Render Trend Cards
// ======================================================

function renderTrends(trends){

    const container =
        document.getElementById("top-trends");

    container.innerHTML = "";

    if(!trends.length){

        container.innerHTML = `

            <div class="no-results">

                <i class="fa-solid fa-magnifying-glass"></i>

                <h3>No Trends Found</h3>

                <p>Try another keyword.</p>

            </div>

        `;

        return;

    }

    trends.forEach(trend=>{

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



// ======================================================
// Search Trends
// ======================================================

async function searchTrends(){

    try{

        const query = document
            .getElementById("searchInput")
            .value
            .trim();

        if(!query){

            loadTopTrends();

            return;

        }

        const data = await apiRequest(

            `/search_trends?query=${encodeURIComponent(query)}`

        );

        renderTrends(data);

    }

    catch(error){

        console.error(error);

        showToast(
            "Search failed.",
            "error"
        );

    }

}



// ======================================================
// Category Filter
// ======================================================

async function loadCategory(category){

    try{

        const trends =
            await apiRequest(`/category/${category}`);

        renderTrends(trends);

    }

    catch(error){

        console.error(error);

        showToast(
            "Unable to load category.",
            "error"
        );

    }

}



document
.querySelectorAll(".category-filter button")
.forEach(button=>{

    button.addEventListener("click",()=>{

        document
        .querySelectorAll(".category-filter button")
        .forEach(btn=>btn.classList.remove("active"));

        button.classList.add("active");

    });

});

// ======================================================
// Predictions
// ======================================================

async function loadPredictions(){

    try{

        const predictions =
            await apiRequest("/predict_trends");

        const container =
            document.getElementById("predictions");

        container.innerHTML = "";

        if(predictions.length===0){

            container.innerHTML = `
                <p>No predictions available.</p>
            `;

            document.getElementById(
                "predictionAverage"
            ).innerText="--";

            return;

        }

        // Average Prediction Score

        const avgPrediction =
            predictions.reduce(

                (sum,item)=>
                    sum + item.predicted_score,

                0

            ) / predictions.length;

        document.getElementById(
            "predictionAverage"
        ).innerText =
            avgPrediction.toFixed(1);


        // Prediction Cards

        predictions.forEach(item=>{

            const color =
                item.trend==="Rising"
                ? "#22c55e"
                : "#ef4444";

            const icon =
                item.trend==="Rising"
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
                            style="color:${color}">

                            ${icon} ${item.trend}

                        </span>

                    </div>

                    <h3>${item.topic}</h3>

                    <div class="prediction-values">

                        <div>

                            <small>Current Score</small>

                            <h4>

                                ${Math.round(item.current_score)}

                            </h4>

                        </div>

                        <div>

                            <small>Predicted Score</small>

                            <h4>

                                ${Math.round(item.predicted_score)}

                            </h4>

                        </div>

                    </div>

                </div>

            `;

        });

    }

    catch(error){

        console.error(error);

        showToast(
            "Unable to load predictions.",
            "error"
        );

    }

}


async function loadCategories() {

    try {

        const data = await apiRequest("/domains");

        const select1 = document.getElementById("category1");
        const select2 = document.getElementById("category2");

        if (!select1 || !select2)
            return;

        select1.innerHTML =
            '<option value="">Select Category</option>';

        select2.innerHTML =
            '<option value="">Select Category</option>';

        data.domains.forEach(category => {

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

    catch (error) {

        console.error(error);

    }

}

async function compareCategories() {

    const cat1 =
        document.getElementById("category1").value;

    const cat2 =
        document.getElementById("category2").value;

    if (!cat1 || !cat2) {

        showToast(
            "Please select both categories.",
            "warning"
        );

        return;

    }

    if (cat1 === cat2) {

        showToast(
            "Choose two different categories.",
            "warning"
        );

        return;

    }

    try {

        const data = await apiRequest(
            `/compare_categories?cat1=${cat1}&cat2=${cat2}`
        );

        renderComparisonCards(
            data[cat1],
            data[cat2]
        );

        drawComparisonChart(
            data[cat1],
            data[cat2]
        );

        generateComparisonSummary(
            data[cat1],
            data[cat2]
        );

    }

    catch(error){

        console.error(error);

    }

}

function renderComparisonCards(cat1, cat2){

    const container =
        document.getElementById(
            "comparison-results"
        );

    if(!container)
        return;

    container.innerHTML = `

        <div class="compare-card">

            <h3>${cat1.category}</h3>

            <p>Articles : ${cat1.articles}</p>

            <p>Average Score : ${cat1.avg_score}</p>

            <p>Prediction : ${cat1.predicted_score}</p>

        </div>

        <div class="compare-card">

            <h3>${cat2.category}</h3>

            <p>Articles : ${cat2.articles}</p>

            <p>Average Score : ${cat2.avg_score}</p>

            <p>Prediction : ${cat2.predicted_score}</p>

        </div>

    `;

}

function drawComparisonChart(cat1, cat2){

    const canvas =
        document.getElementById("comparisonChart");

    if(!canvas)
        return;

    const ctx =
        canvas.getContext("2d");

    if(comparisonChart){

        comparisonChart.destroy();

    }

    comparisonChart =
    new Chart(ctx,{

        type:"bar",

        data:{

            labels:[
                "Articles",
                "Average Score",
                "Prediction",
                "Growth"
            ],

            datasets:[

                {

                    label:cat1.category,

                    data:[
                        cat1.articles,
                        cat1.avg_score,
                        cat1.predicted_score,
                        cat1.growth
                    ]

                },

                {

                    label:cat2.category,

                    data:[
                        cat2.articles,
                        cat2.avg_score,
                        cat2.predicted_score,
                        cat2.growth
                    ]

                }

            ]

        }

    });

}

function generateComparisonSummary(cat1, cat2) {

    const winner =
        cat1.predicted_score > cat2.predicted_score
        ? cat1
        : cat2;

    const loser =
        winner.category === cat1.category
        ? cat2
        : cat1;

    const scoreDifference =
        Math.abs(
            winner.predicted_score -
            loser.predicted_score
        ).toFixed(1);

    document.getElementById("comparison-summary").innerHTML = `

        <h3>🤖 AI Insight</h3>

        <table class="summary-table">

            <tr>
                <td><strong>Leading Category</strong></td>
                <td>${winner.category.toUpperCase()}</td>
            </tr>

            <tr>
                <td><strong>Current Articles</strong></td>
                <td>${winner.articles}</td>
            </tr>

            <tr>
                <td><strong>Average Trend Score</strong></td>
                <td>${winner.avg_score}</td>
            </tr>

            <tr>
                <td><strong>Predicted Score</strong></td>
                <td>${winner.predicted_score}</td>
            </tr>

            <tr>
                <td><strong>Growth</strong></td>
                <td>+${winner.growth}%</td>
            </tr>

            <tr>
                <td><strong>Winning Margin</strong></td>
                <td>${scoreDifference}</td>
            </tr>

        </table>

        <br>

        <p>

        Based on the current trend score, article volume and prediction model,
        <strong>${winner.category.toUpperCase()}</strong> is expected to
        outperform <strong>${loser.category.toUpperCase()}</strong> in the
        coming days.

        </p>

    `;
}


// ======================================================
// Dashboard Stats
// ======================================================

async function loadDashboardStats(){

    try{

        const trends =
            await apiRequest("/all_trends");

        document.getElementById("articles").innerText =
            trends.length;

        const avgScore =

            trends.reduce(

                (sum,item)=>
                    sum + item.trend_score,

                0

            ) / trends.length;

        document.getElementById(
            "avg-score"
        ).innerText =
            avgScore.toFixed(1);

    }

    catch(error){

        console.error(error);

        showToast(
            "Unable to load statistics.",
            "error"
        );

    }

}



// ======================================================
// Trend Score Chart
// ======================================================

async function loadTrendChart(){

    try{

        const data =
            await apiRequest("/category_stats");

        data.sort(
            (a,b)=>
                b.avg_score-a.avg_score
        );

        const labels =
            data.map(item=>item.category);

        const scores =
            data.map(item=>item.avg_score);

        const ctx =
            document
                .getElementById("trendChart")
                .getContext("2d");


        // Prevent duplicate chart

        if(trendChart){

            trendChart.destroy();

        }


        trendChart = new Chart(ctx,{

            type:"bar",

            data:{

                labels:labels,

                datasets:[{

                    label:"Average Trend Score",

                    data:scores,

                    borderWidth:1,

                    borderRadius:8

                }]

            },

            options:{

                responsive:true,

                maintainAspectRatio:false,

                plugins:{

                    legend:{

                        labels:{

                            color:"white"

                        }

                    }

                },

                scales:{

                    x:{

                        ticks:{

                            color:"white"

                        },

                        grid:{

                            color:"rgba(255,255,255,.08)"

                        }

                    },

                    y:{

                        beginAtZero:true,

                        max:100,

                        ticks:{

                            color:"white"

                        },

                        grid:{

                            color:"rgba(255,255,255,.08)"

                        }

                    }

                }

            }

        });

    }

    catch(error){

        console.error(error);

        showToast(
            "Unable to load trend chart.",
            "error"
        );

    }

}

// ======================================
// ANALYTICS DASHBOARD
// ======================================

let distributionChart = null;

async function loadAnalyticsDashboard() {

    try {

        const data = await apiRequest(
            "/category_stats"
        );

        data.sort((a, b) => b.avg_score - a.avg_score);

        const totalArticles =
            data.reduce(
                (sum, item) => sum + item.articles,
                0
            );

        const averageScore =
            data.reduce(
                (sum, item) => sum + item.avg_score,
                0
            ) / data.length;

        document.getElementById(
            "analyticsArticles"
        ).innerText = totalArticles;

        document.getElementById(
            "analyticsAverage"
        ).innerText = averageScore.toFixed(1);

        document.getElementById(
            "topCategory"
        ).innerText =
            data[0].category.toUpperCase();

        if (!document.getElementById("predictionAverage").innerText.trim()) {

            document.getElementById(
                "predictionAverage"
            ).innerText = "--";

        }

        // Destroy old charts

        if (distributionChart) {
            distributionChart.destroy();
        }

        if (topCategoryChart) {
            topCategoryChart.destroy();
        }

        // =====================
        // Doughnut Chart
        // =====================

        distributionChart = new Chart(

            document.getElementById(
                "categoryDistributionChart"
            ),

            {

                type: "doughnut",

                data: {

                    labels: data.map(
                        item => item.category
                    ),

                    datasets: [{

                        data: data.map(
                            item => item.articles
                        )

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

        // =====================
        // Horizontal Bar Chart
        // =====================

        topCategoryChart = new Chart(

            document.getElementById(
                "topCategoriesChart"
            ),

            {

                type: "bar",

                data: {

                    labels: data.map(
                        item => item.category
                    ),

                    datasets: [{

                        label: "Average Trend Score",

                        data: data.map(
                            item => item.avg_score
                        )

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

        console.error(error);

        showToast(
            "Unable to load analytics dashboard.",
            "error"
        );

    }

}

// ======================================
// CATEGORY INSIGHTS
// ======================================

async function loadCategoryInsights() {

    try {

        const data = await apiRequest(
            "/category_stats"
        );

        data.sort((a, b) => b.avg_score - a.avg_score);

        const container =
            document.getElementById("categoryInsights");

        if (!container) return;

        container.innerHTML = "";

        data.forEach((item, index) => {

            let performance = "Average";

            if (item.avg_score >= 80)
                performance = "Excellent";

            else if (item.avg_score >= 70)
                performance = "Good";

            container.innerHTML += `

                <div class="insight-card">

                    <h3>${item.category.toUpperCase()}</h3>

                    <p><strong>Articles:</strong> ${item.articles}</p>

                    <p><strong>Average Score:</strong> ${item.avg_score}</p>

                    <p><strong>Rank:</strong> #${index + 1}</p>

                    <span class="performance">

                        ${performance}

                    </span>

                </div>

            `;

        });

    }

    catch (error) {

        console.error(error);

        showToast(
            "Unable to load category insights.",
            "error"
        );

    }

}


// ======================================
// ERROR POPUP
// ======================================

function showError(message) {

    const popup =
        document.getElementById("error-popup");

    const text =
        document.getElementById("error-text");

    if (!popup || !text)
        return;

    text.innerText = message;

    popup.classList.add("show");

    setTimeout(() => {

        popup.classList.remove("show");

    }, 3000);

}


// ======================================
// INITIALIZE DASHBOARD
// ======================================

async function initializeDashboard() {

    try {

        showLoader();

        await Promise.all([

            loadProfile(),

            loadDashboardStats(),

            loadTopTrends(),

            loadPredictions(),

            loadCategories(),

            loadAnalyticsDashboard(),

            loadCategoryInsights()

        ]);

        showToast(
            "Dashboard loaded successfully!",
            "success"
        );

    }

    catch (error) {

        console.error(error);

        showToast(
            "Failed to load dashboard.",
            "error"
        );

    }

    finally {

        hideLoader();

    }

}


// ======================================
// START APPLICATION
// ======================================

initializeDashboard();