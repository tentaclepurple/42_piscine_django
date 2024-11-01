# ex02/forms.py
from django import forms


class TextInputForm(forms.Form):
    text = forms.CharField(label='Enter Text', max_length=100)
