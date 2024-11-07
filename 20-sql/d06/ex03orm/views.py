from .data import data
from django.http import HttpResponse
from .models import Movies


def list_to_dict():
    movies_list = []
    for episode in data:
        movie_data = {
            "episode_nb": episode[0],
            "title": episode[1],
            "director": episode[2],
            "producer": episode[3],
            "release_date": episode[4],
        }
        movies_list.append(movie_data)
    return movies_list

def populate(request):
    results = []
    movies_data = list_to_dict()

    for movie_data in movies_data:
        try:
            movie = Movies(**movie_data)
            movie.save()
            results.append(f"OK: {movie.title}")
        except Exception as e:
            results.append(f"Error: {movie_data['title']} - {e}")

    return HttpResponse("<br>".join(results))


def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")

        html = "<table border='1'><tr><th>Episode</th><th>Title</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
        for movie in movies:
            html += f"<tr><td>{movie.episode_nb}</td><td>{movie.title}</td><td>{movie.opening_crawl or ''}</td><td>{movie.director}</td><td>{movie.producer}</td><td>{movie.release_date}</td></tr>"
        html += "</table>"

        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")
