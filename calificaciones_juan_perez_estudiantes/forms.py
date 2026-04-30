from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        exclude = ['promedio']

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
