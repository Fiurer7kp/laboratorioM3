from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinLengthValidator
from .models import Calificacion
from .forms import CalificacionForm

# Formulario de registro personalizado COMPLETAMENTE EN ESPAÑOL
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    # Personalizar el campo username (nombre de usuario)
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        help_text="Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Personalizar el campo password1 (contraseña)
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        help_text="""
        <ul class='small text-muted'>
            <li>Tu contraseña no puede ser demasiado similar a tu otra información personal.</li>
            <li>Tu contraseña debe contener al menos 8 caracteres.</li>
            <li>Tu contraseña no puede ser una contraseña comúnmente usada.</li>
            <li>Tu contraseña no puede ser completamente numérica.</li>
        </ul>
        """
    )
    
    # Personalizar el campo password2 (confirmación)
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        help_text="Ingrese la misma contraseña que antes, para verificación."
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, '✅ Registro exitoso. ¡Bienvenido!')
            return redirect('listar')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

# Vista de login personalizada con mensajes diferenciados
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            messages.error(request, '❌ Usuario no registrado')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'✅ ¡Bienvenido de nuevo, {username}!')
            return redirect('listar')
        else:
            messages.error(request, '❌ Contraseña incorrecta')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# CRUD de calificaciones
@login_required
def listar(request):
    calificaciones = Calificacion.objects.all().order_by('-id')
    promedio_general = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg'] or 0
    return render(request, 'calificaciones/listar.html', {
        'calificaciones': calificaciones,
        'promedio_general': round(promedio_general, 2),
    })

@login_required
def crear(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Calificación creada exitosamente.')
            return redirect('listar')
    else:
        form = CalificacionForm()
    return render(request, 'calificaciones/crear.html', {'form': form})

@login_required
def editar(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Calificación actualizada correctamente.')
            return redirect('listar')
    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificaciones/editar.html', {'form': form, 'calificacion': calificacion})

@login_required
def eliminar(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, '✅ Calificación eliminada correctamente.')
        return redirect('listar')
    return render(request, 'calificaciones/eliminar.html', {'calificacion': calificacion})
