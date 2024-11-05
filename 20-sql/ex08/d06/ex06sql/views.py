from django.http import HttpResponse
import psycopg2
import environ
from django.shortcuts import redirect, render
from django import forms
from django.views.decorators.csrf import csrf_exempt
from .queries import populate_ex06_movies_query, create_ex06_movies_query
from .queries import trigger_function, trigger 
from .data import data


env = environ.Env()
env.read_env("../../.env")


DB_NAME = env("POSTGRES_DB")
DB_USER = env("POSTGRES_USER")
DB_PASSWORD = env("POSTGRES_PASSWORD")
DB_HOST = env("POSTGRES_HOST", default="localhost")
DB_PORT = env("POSTGRES_PORT", default="30432")


class MovieRemoveForm(forms.Form):
    title = forms.ChoiceField(label="Select a movie to remove")


def init(request):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        cursor = conn.cursor()
        
        cursor.execute(create_ex06_movies_query)
        cursor.execute(trigger_function)
        cursor.execute(trigger)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return HttpResponse("OK")
    
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    results = []
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cursor = conn.cursor()

        for episode in data:
            try:
                cursor.execute(populate_ex06_movies_query, episode)
                conn.commit()
                results.append(f"OK: {episode[1]}")
            except psycopg2.IntegrityError as e:
                conn.rollback()
                results.append(f"Error: {episode[1]} - {e}")
            except Exception as e:
                conn.rollback()
                results.append(f"Error: {episode[1]} - {e}")

        cursor.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Error: {e}")

    return HttpResponse("<br>".join(results))


def display(request):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
		)
        
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ex06sql_movies')
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        html = "<table border='1'><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
        for row in rows:
            html += "<tr>" + "".join(f"<td>{col if col else ''}</td>" for col in row) + "</tr>"
        html += "</table>"
        
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"No data available")


@csrf_exempt
def remove(request):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        if request.method == "POST":
            title = request.POST.get("title")
            cursor.execute("DELETE FROM ex06sql_movies WHERE title = %s", [title])
            conn.commit()
            return redirect("ex06sql:remove")

        cursor.execute("SELECT title FROM ex06sql_movies")
        movies = cursor.fetchall()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        form = MovieRemoveForm()
        form.fields["title"].choices = [(movie[0], movie[0]) for movie in movies]

        html = "<form method='post'>" + form.as_p() + "<button type='submit'>Remove</button></form>"
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse("No data available")


class UpdateOpeningCrawlForm(forms.Form):
    title = forms.ChoiceField(label="Select a movie to update")
    opening_crawl = forms.CharField(widget=forms.Textarea, label="Opening Crawl")


@csrf_exempt
def update(request):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        if request.method == "POST":
            title = request.POST.get("title")
            opening_crawl = request.POST.get("opening_crawl")
            cursor.execute(
                "UPDATE ex06sql_movies SET opening_crawl = %s WHERE title = %s",
                (opening_crawl, title)
            )
            conn.commit()
            return redirect("ex06sql:update")

        cursor.execute("SELECT title FROM ex06sql_movies")
        movies = cursor.fetchall()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        form = UpdateOpeningCrawlForm()
        form.fields["title"].choices = [(movie[0], movie[0]) for movie in movies]

        return render(request, "ex06/update.html", {"form": form})
    except Exception as e:
        return HttpResponse("No data available")
