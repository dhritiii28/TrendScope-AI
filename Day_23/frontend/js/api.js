const BASE_URL = "http://127.0.0.1:8000";

async function apiRequest(endpoint, options = {}) {

    try {

        const response = await fetch(BASE_URL + endpoint, {

            headers: {

                "Authorization": token
                    ? `Bearer ${token}`
                    : "",

                "Content-Type": "application/json",

                ...options.headers

            },

            ...options

        });

        if (!response.ok) {

            throw new Error(
                `Server Error (${response.status})`
            );

        }

        return await response.json();

    }

    catch (error) {

        console.error(error);

        showError(error.message);

        throw error;

    }

}