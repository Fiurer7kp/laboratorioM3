from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Calificacion
from .forms import CalificacionForm
from django.contrib import messages

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
            form.save()messages.success(request, 'Calificación creada exitosamente.')
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
            form.save()messages.success(request, 'Calificación actualizada.')
            return redirect('listar')
    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificaciones/editar.html', {'form': form})

@login_required
def eliminar(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        calificacion.delete()messages.success(request, 'Calificación eliminada.')
        return redirect('listar')
    return render(request, 'calificaciones/eliminar.html', {'calificacion': calificacion})
from django.contrib import messages
# Modificar las vistas crear, editar, eliminar para agregar mensajes
