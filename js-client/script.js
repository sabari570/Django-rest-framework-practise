document
  .getElementById("loginForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the form from reloading the page

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const payload = {
      username: username,
      password: password,
    };

    try {
      const response = await fetch("http://localhost:8000/api/auth/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("API Response:", data);
    } catch (error) {
      console.error("Error calling the API:", error);
    }
  });
