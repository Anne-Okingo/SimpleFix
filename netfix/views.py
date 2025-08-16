from django.shortcuts import render

from users.models import User, Company, Customer
from services.models import Service
from django.shortcuts import render
from services.models import ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, username):
    # Fetch the customer user
    user = User.objects.get(username=username)
    
    # Fetch all service requests made by this customer, ordered by most recent
    service_requests = ServiceRequest.objects.filter(
        customer=Customer.objects.get(user=user)
    ).order_by("-requested_at")
    
    return render(request, 'users/customer_profile.html', {
        'user': user,
        'service_requests': service_requests
    })

def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-created_at")

    return render(request, 'users/profile_company.html', {'user': user, 'services': services})
