from django.http import HttpResponse
import psycopg2
import environ
from .queries import create_ex00_movies_sql


env = environ.Env()


def init(request):
    try:
        conn = psycopg2.connect(
            dbname=env("POSTGRES_DB"),
            user=env("POSTGRES_USER"),
            password=env("POSTGRES_PASSWORD"),
            host=env("POSTGRES_HOST", default="localhost"),
            port=env("POSTGRES_PORT", default="30432")
        )
        cursor = conn.cursor()
        
        cursor.execute(create_ex00_movies_sql)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return HttpResponse("OK")
    
    except Exception as e:
        # Si hay un error, retornar el mensaje de error
        return HttpResponse(f"Error: {e}")
