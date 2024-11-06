# ex10/forms.py

from django import forms
from .models import People

class SearchForm(forms.Form):
    min_release_date = forms.DateField(
        label="Movies Minimum Release Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    max_release_date = forms.DateField(
        label="Movies Maximum Release Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    min_diameter = forms.IntegerField(
        label="Planet Diameter Greater Than",
        min_value=0
    )
    gender = forms.ChoiceField(
        label="Character Gender",
        choices=[]  # To be populated dynamically
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        genders = People.objects.values_list('gender', flat=True).distinct()
        gender_choices = [(gender, gender.capitalize()) for gender in genders if gender]
        self.fields['gender'].choices = gender_choices
