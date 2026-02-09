const form = document.getElementById("predictForm");
const result = document.getElementById("result");
const loader = document.getElementById("loader");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    loader.classList.remove("hidden");
    result.innerHTML = "";

    const formData = new FormData(form);

    let data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const res = await response.json();

    loader.classList.add("hidden");

    if (res.success) {
        result.innerHTML =
            `🎯 Predicted Maths Score: <b>${res.prediction}</b>`;
    } else {
        result.innerHTML =
            `❌ Error: ${res.error || "Something went wrong"}`;
    }

});

