from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.forms import AuthenticationForm
from .models import Calificacion
from .forms import CalificacionForm, RegistroUsuarioForm

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido.')
            return redirect('listar')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

# Vista de login personalizada con mensajes específicos
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth.models import User
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            messages.error(request, '❌ Usuario no registrado')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('listar')
        else:
            messages.error(request, '❌ Contraseña incorrecta')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# CRUD
@login_required
def listar(request):
    calificaciones = Calificacion.objects.all()
    promedio_general = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg'] or 0
    return render(request, 'calificaciones/listar.html', {'calificaciones': calificaciones, 'promedio_general': promedio_general})

@login_required
def crear(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calificación creada exitosamente.')
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
            messages.success(request, 'Calificación actualizada correctamente.')
            return redirect('listar')
    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificaciones/editar.html', {'form': form})

@login_required
def eliminar(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, 'Calificación eliminada correctamente.')
        return redirect('listar')
    return render(request, 'calificaciones/eliminar.html', {'calificacion': calificacion})
