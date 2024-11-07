from django.http import HttpResponse
import psycopg2
from django.conf import settings
import environ
from .queries import populate_ex02_movies_query, create_ex02_movies_query, data


env = environ.Env()
env.read_env("../../.env")

DB_NAME = env("POSTGRES_DB")
DB_USER = env("POSTGRES_USER")
DB_PASSWORD = env("POSTGRES_PASSWORD")
DB_HOST = env("POSTGRES_HOST", default="localhost")
DB_PORT = env("POSTGRES_PORT", default="30432")


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
        
        cursor.execute(create_ex02_movies_query)
        
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
                cursor.execute(populate_ex02_movies_query, episode)
                results.append(f"OK: {episode[1]}")
            except Exception as e:
                results.append(f"Error: {episode[1]} - {e}")

        conn.commit()
        
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
        cursor.execute('SELECT * FROM ex02sql_movies')
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
