from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import Company, Customer
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

# ------------------------------------------------------------------------
# List all services (newest first)
# ------------------------------------------------------------------------
def service_list(request):
    services = Service.objects.all().order_by("-created_at")
    return render(request, 'services/list.html', {'services': services})

# ------------------------------------------------------------------------
# Single service detail page
# ------------------------------------------------------------------------
def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    form = None

    # Only customers can request services
    if request.user.is_authenticated and request.user.is_customer:
        if request.method == 'POST':
            form = RequestServiceForm(request.POST)
            if form.is_valid():
                customer = request.user.customer
                ServiceRequest.objects.create(
                    service=service,
                    customer=customer,
                    address=form.cleaned_data['address'],
                    hours=form.cleaned_data['hours']
                )
                return redirect('customer_profile', name=request.user.username)
        else:
            form = RequestServiceForm()

    return render(request, 'services/single_service.html', {'service': service, 'form': form})

# ------------------------------------------------------------------------
# Create a new service (only for companies)
# ------------------------------------------------------------------------
@login_required
def create_service(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        return redirect('login')  # Only companies can create services

    if request.method == 'POST':
        form = CreateNewService(request.POST, company=company)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = company
            service.save()
            return redirect('company_profile', name=request.user.username)
    else:
        form = CreateNewService(company=company)

    return render(request, 'services/create_service.html', {'form': form})

# ------------------------------------------------------------------------
# Services filtered by field/category
# ------------------------------------------------------------------------
def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})

# ------------------------------------------------------------------------
# Request a service (old version, now handled inside service_detail)
# ------------------------------------------------------------------------
@login_required
def request_service(request, id):
    service = get_object_or_404(Service, id=id)

    if not request.user.is_customer:
        return redirect('login')

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            customer = request.user.customer
            ServiceRequest.objects.create(
                service=service,
                customer=customer,
                address=form.cleaned_data['address'],
                hours=form.cleaned_data['hours']
            )
            return redirect('customer_profile', name=request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'service': service, 'form': form})
