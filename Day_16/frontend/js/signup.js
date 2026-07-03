async function registerUser() {

    const userData = {

        id: Number(
            document.getElementById("id").value
        ),

        username:
            document.getElementById("username").value,

        email:
            document.getElementById("email").value,

        password:
            document.getElementById("password").value
    };

    const response = await fetch(
        "http://127.0.0.1:8000/register",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(userData)
        }
    );

    const data = await response.json();

    document.getElementById("message").innerText =
        data.message;
}