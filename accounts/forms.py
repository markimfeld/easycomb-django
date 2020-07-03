from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField (
        widget = forms.TextInput (
            attrs = {
                'placeholder': 'Usuario',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField (
        widget = forms.PasswordInput (
            attrs = {
                'placeholder': 'Contraseña',
                'class': 'form-control'
            }
        )
    )
