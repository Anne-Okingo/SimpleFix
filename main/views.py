from django.shortcuts import render
from services.models import Service
from django.contrib.auth import logout as django_logout


def home(request):
    services = Service.objects.all()
    return render(request, 'main/home.html', {'services': services})


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
