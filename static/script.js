document.getElementById("getMovie").addEventListener("click", function() {
    let genre = document.getElementById("genre").value; 
    let year = document.getElementById("year").value;
    let min_rating = Math.min(10, Math.max(0, Math.round(document.getElementById("min_rating").value || 0)));
    let language = document.getElementById("language").value;

    let url = `/random_movie?genre=${genre}&year=${year}&min_rating=${min_rating}&language=${language}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById("movieTitle").innerText = data.title;
        document.getElementById("movieOverview").innerText = data.overview;
        document.getElementById("movieDuration").innerText = data.duration;
        document.getElementById("movieActors").innerText = data.actors.join(", ");
        document.getElementById("movieRating").innerText = data.imdb_rating;

        let poster = document.getElementById("moviePoster");
        poster.src = data.poster;

        let trailer = document.getElementById("trailerLink");
        if (data.trailer) {
            trailer.href = data.trailer;
            trailer.style.display = "block";
        } else {
            trailer.style.display = "none";
        }
    })
    .catch(error => console.error("Error:", error));
});
