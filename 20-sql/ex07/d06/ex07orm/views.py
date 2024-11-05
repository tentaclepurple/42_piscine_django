from .data import data
from django.http import HttpResponse
from .models import Movies
from django import forms
from django.shortcuts import redirect, render


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
            movie, created = Movies.objects.get_or_create(**movie_data)
            if created:
                results.append(f"OK: {movie.title}")
            else:
                results.append(f"{movie.title} already exists.")
        except Exception as e:
            results.append(f"Error: {movie_data['title']} - {e}")

    return HttpResponse("<br>".join(results))


def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")

        html = "<table border='1'><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th><th>Created</th><th>Updated</th></tr>"
        for movie in movies:
            html += f"<tr><td>{movie.title}</td><td>{movie.episode_nb}</td><td>{movie.opening_crawl or ''}</td><td>{movie.director}</td><td>{movie.producer}</td><td>{movie.release_date}</td><td>{movie.created}</td><td>{movie.updated}</td></tr>"
        html += "</table>"

        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")


class MovieRemoveForm(forms.Form):
    title = forms.ChoiceField(label="Select a movie to remove")


def remove(request):
    if request.method == "POST":
        title = request.POST.get("title")
        Movies.objects.filter(title=title).delete()
        return redirect("ex07orm:remove")

    movies = Movies.objects.all()
    if not movies.exists():
        return HttpResponse("No data available")

    form = MovieRemoveForm()
    form.fields["title"].choices = [(movie.title, movie.title) for movie in movies]

    return render(request, "ex07/remove.html", {"form": form})


class UpdateOpeningCrawlForm(forms.Form):
    title = forms.ChoiceField(label="Select a movie to update")
    opening_crawl = forms.CharField(widget=forms.Textarea, label="Opening Crawl")


def update(request):
    # Crear el formulario con las opciones correctas para GET y POST
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")

    form = UpdateOpeningCrawlForm(request.POST or None)
    form.fields["title"].choices = [(movie.title, movie.title) for movie in movies]

    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        opening_crawl = form.cleaned_data["opening_crawl"]

        try:
            movie = Movies.objects.get(title=title)
            movie.opening_crawl = opening_crawl
            movie.save()
            return redirect("ex07orm:update")
        except Movies.DoesNotExist:
            return HttpResponse("Movie not found", status=404)
    elif request.method == "POST":
        print("Form is invalid:", form.errors)

    return render(request, "ex07/update.html", {"form": form})
