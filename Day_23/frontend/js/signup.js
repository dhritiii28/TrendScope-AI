async function registerUser() {

    const userData = {

        username: document.getElementById("username").value,

        email: document.getElementById("email").value,

        password: document.getElementById("password").value
    };

    const response = await fetch(
        "http://127.0.0.1:8000/register",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        }
    );

    console.log("Status:", response.status);

    const data = await response.json();

    console.log("Response:", data);

    document.getElementById("message").innerText =
        data.message || data.detail || JSON.stringify(data);
}