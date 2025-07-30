from flask import Flask, render_template, request, jsonify
import requests
import random
from config import TMDB_API_KEY, OMDB_API_KEY

app = Flask(__name__)

def get_imdb_rating(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    return response.get("imdbRating", "N/A")

def get_random_movie(genre=None, year=None, min_rating=None, language="en"):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=es-ES&sort_by=popularity.desc&page=1"

    if genre:
        url += f"&with_genres={genre}"
    if year:
        url += f"&primary_release_year={year}"
    else:
        url += f"&primary_release_date.gte=2015-01-01" 
        
    if min_rating:
        url += f"&vote_average.gte={min_rating}"

    url += "&vote_count.gte=50"  
    url += "&with_runtime.gte=60"

    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json().get("results", [])
        if movies:
            movie = random.choice(movies)

            movie_id = movie["id"]
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,videos"
            details_response = requests.get(details_url).json()

            actors = [actor["name"] for actor in details_response.get("credits", {}).get("cast", [])[:3]]
            videos = details_response.get("videos", {}).get("results", [])
            trailer_key = next((v["key"] for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
            trailer_url = f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None

            poster_path = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"

            return {
                "title": movie["title"],
                "overview": movie["overview"],
                "poster": poster_url,
                "duration": details_response.get("runtime", "Desconocida"),
                "actors": actors,
                "trailer": trailer_url
            }

    return {"title": "No se encontraron películas", "overview": "", "poster": "https://via.placeholder.com/500x750?text=No+Image", "duration": "N/A", "actors": [], "trailer": None}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/random_movie")
def random_movie():
    genre = request.args.get("genre") 
    year = request.args.get("year")
    min_rating = request.args.get("min_rating")
    language = request.args.get("language")

    movie = get_random_movie(genre, year, min_rating, language)
    return jsonify(movie)


if __name__ == "__main__":
    app.run(debug=True)
