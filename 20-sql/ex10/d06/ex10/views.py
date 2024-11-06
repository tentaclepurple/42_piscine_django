# ex10/views.py

from django.shortcuts import render
from .forms import SearchForm
from .models import People, Movies, Planets
from django.db.models import Q


def display(request):
    results = []
    message = ""
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            min_release_date = form.cleaned_data['min_release_date']
            max_release_date = form.cleaned_data['max_release_date']
            min_diameter = form.cleaned_data['min_diameter']
            gender = form.cleaned_data['gender']

            # Fetch person-movie pairs that match all criteria
            matching_pairs = People.objects.filter(
                gender__iexact=gender,
                homeworld__diameter__gte=min_diameter,
                movies__release_date__range=(min_release_date, max_release_date)
            ).select_related('homeworld').values(
                'name',
                'gender',
                'movies__title',
                'homeworld__name',
                'homeworld__diameter'
            ).distinct()

            results = list(matching_pairs)

            if not results:
                message = "Nothing corresponding to your research"
    else:
        form = SearchForm()

    context = {
        'form': form,
        'results': results,
        'message': message
    }
    return render(request, 'ex10/display.html', context)
