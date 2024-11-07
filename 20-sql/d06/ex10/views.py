from django.shortcuts import render
from .models import Movies, People, Planets
from django.db.models import Q, Count, Prefetch
from datetime import datetime

def display(request):
    # Obtener valores únicos para el campo de género
    genders = People.objects.values_list('gender', flat=True).distinct()
    results = []

    # Verificar que todos los parámetros necesarios están en la solicitud GET
    if request.method == 'GET' and all(field in request.GET for field in ('min_date', 'max_date', 'diameter', 'gender')):
        # Obtener valores de los filtros de la solicitud
        min_date_str = request.GET.get('min_date')
        max_date_str = request.GET.get('max_date')
        diameter_str = request.GET.get('diameter')
        gender = request.GET.get('gender')

        # Convertir fechas de cadena a objetos datetime para evitar problemas de formato
        try:
            min_date = datetime.strptime(min_date_str, "%Y-%m-%d").date()
            max_date = datetime.strptime(max_date_str, "%Y-%m-%d").date()
        except ValueError:
            # Si el formato es incorrecto, renderizamos el formulario con un mensaje de error
            return render(request, 'ex10/ex10.html', {
                'genders': genders,
                'results': [],
                'error': 'Las fechas deben estar en el formato YYYY-MM-DD.'
            })

        # Convertir diameter a entero
        try:
            diameter = int(diameter_str)
        except ValueError:
            return render(request, 'ex10/ex10.html', {
                'genders': genders,
                'results': [],
                'error': 'El diámetro debe ser un número entero.'
            })

        # Filtrar películas dentro del rango de fechas
        movies_in_date_range = Movies.objects.filter(
            release_date__gte=min_date,
            release_date__lte=max_date
        )

        # Obtener personas que cumplen con los criterios de filtrado
        results = People.objects.filter(
            gender=gender,
            homeworld__diameter__gte=diameter,
            movies__in=movies_in_date_range
        ).distinct()

        # Prefetchear las películas filtradas y planetas relacionados
        results = results.prefetch_related(
            Prefetch(
                'movies',
                queryset=movies_in_date_range,
                to_attr='filtered_movies'
            ),
            'homeworld'
        )

    # Renderizar plantilla con los resultados y los géneros
    return render(request, 'ex10/ex10.html', {'genders': genders, 'results': results})
