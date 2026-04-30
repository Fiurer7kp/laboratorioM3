from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from calificaciones_juan_perez_estudiantes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('', include('calificaciones_juan_perez_estudiantes.urls')),
]
