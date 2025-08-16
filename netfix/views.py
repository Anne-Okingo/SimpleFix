from django.shortcuts import render, get_object_or_404


from users.models import User, Company, Customer, Service
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
    # Get the company for this username
    company = get_object_or_404(Company, user__username=name)
    # Get all services for this company, newest first
    services = company.services.all().order_by('-created_at')

    return render(request, 'users/profile_company.html', {
        'company': company,
        'services': services
    })