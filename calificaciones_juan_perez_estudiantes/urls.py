from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', login_required(home), name='home'),
]
