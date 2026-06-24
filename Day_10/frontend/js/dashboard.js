const token =
    localStorage.getItem("token");

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

loadProfile();