from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import Tip


User = get_user_model()


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Este nombre de usuario ya existe.')
        
        elif password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Wrong credentials.")
        
        self.user = user

        return cleaned_data

    def get_user(self):
        return self.user
