from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from .models import People


def display(request):
    people = People.objects.filter(
        Q(homeworld__climate__icontains='windy') |
        Q(homeworld__climate__icontains='moderately windy')
    ).order_by('name')

    if not people.exists():
        return HttpResponse("No data available, please use the following "
                            "command line before use:<br>python manage.py "
                            "loaddata ex09_initial_data.json")

    context = {
        'people': people
    }
    return render(request, 'ex09/display.html', context)
