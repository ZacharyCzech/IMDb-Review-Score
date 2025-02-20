let currentImdbId = "";

document.getElementById("importButton").addEventListener("click", () => {
    const imdbInput = document.getElementById("imdb_id").value.trim();
    if (!imdbInput) {
        alert("Please enter a valid IMDb ID (e.g. tt0111161)");
        return;
    }
    currentImdbId = imdbInput;
    document.getElementById("status").textContent = "IMDb ID submitted. Updating movie data...";
    eel.get_movie_data(currentImdbId)().then((data) => {
        console.log("Data received:", data); // Debug log
        document.getElementById("title").textContent = (data.title || "N/A");
        document.getElementById("poster").src = data.poster_url || "placeholder.png";
        document.getElementById("avgRating").textContent = data.avg_rating || "N/A";
        document.getElementById("numRatings").textContent = data.rating_count || "N/A";
        document.getElementById("reviewCount").textContent = data.review_count || "N/A";
        document.getElementById("status").textContent = "IMDb ID imported.";
    }).catch((err) => {
        console.error(err);
        document.getElementById("status").textContent = "Error importing the IMDb ID!";
    });
});

document.getElementById("analyzeButton").addEventListener("click", () => {
    if (!currentImdbId) {
        alert("Please submit an IMDb ID first.");
        return;
    }
    document.getElementById("status").textContent = "Analysis in progress...";
    eel.start_analysis(currentImdbId)().then((data) => {
        document.getElementById("status").textContent = "Score calculated!";
        document.getElementById("posPct").textContent = data.pos_pct;
    }).catch((err) => {
        console.error(err);
        document.getElementById("status").textContent = "Failed to calculate the score!";
    });
});

document.getElementById("darkModeToggle").addEventListener("change", (event) => {
    const body = document.querySelector("body");
    const modeIcon = document.getElementById("modeIcon");
    if (event.target.checked) {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        modeIcon.src = "img/icon/light-mode.svg";
        modeIcon.alt = "Switch To Light Mode";
    } else {
        body.classList.remove("dark-mode");
        body.classList.add("light-mode");
        modeIcon.src = "img/icon/dark-mode.svg";
        modeIcon.alt = "Switch To Dark Mode";
    }
});
