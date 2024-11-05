from django.http import HttpResponse
from django.conf import settings
import psycopg2
import environ
from .queries import create_ex08_planets, create_ex08_people, get_people_with_homeworld_climate
import os


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
        
        cursor.execute(create_ex08_planets)
        cursor.execute(create_ex08_people)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return HttpResponse("OK")
    
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

def populate(request):

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cursor = conn.cursor()

        planets_path = os.path.join(settings.BASE_DIR, 'ex08sql', 'data', 'planets.csv')
        with open(planets_path, 'r') as f:
            cursor.copy_from(
                f,
                'ex08sql_planets',
                sep='\t',
                columns=('name', 'climate', 'diameter', 'orbital_period',
                         'population', 'rotation_period', 'surface_water', 'terrain'),
                null="NULL"
            )

        people_path = os.path.join(settings.BASE_DIR, 'ex08sql', 'data', 'people.csv')
        with open(people_path, 'r') as f:
            cursor.copy_from(
                f,
                'ex08sql_people',
                sep='\t',
                columns=('name', 'birth_year', 'gender', 'eye_color', 'hair_color',
                         'height', 'mass', 'homeworld'),
                null="NULL"
            )

        conn.commit()
        cursor.close()
        conn.close()

        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

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

        cursor.execute(get_people_with_homeworld_climate)
        
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        html = "<table border='1'><tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        html += "</table>"

        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"No data available")
