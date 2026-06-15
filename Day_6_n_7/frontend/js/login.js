async function loginUser() {

    const loginData = {

        email:
            document.getElementById("email").value,

        password:
            document.getElementById("password").value
    };

    const response = await fetch(
        "http://127.0.0.1:8000/login",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(loginData)
        }
    );

    const data = await response.json();

    if (data.access_token) {

        localStorage.setItem(
            "token",
            data.access_token
        );

        document.getElementById("message").innerText =
            "Login Successful";

        window.location.href =
            "dashboard.html";

    } else {

        document.getElementById("message").innerText =
            data.detail;
    }
}