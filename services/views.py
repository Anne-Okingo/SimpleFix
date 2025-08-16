from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Company
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

# ------------------------------------------------------------------------
# List all services (newest first)
# ------------------------------------------------------------------------
def service_list(request):
    services = Service.objects.all().order_by("-created_at")
    return render(request, 'services/list.html', {'services': services})

# ------------------------------------------------------------------------
# Single service detail page + request form
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

                 # Add the success message
                messages.success(request, "Service requested successfully!")
                
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
        form = CreateNewService(request.POST, choices=[(company.field, company.field)] if company.field != 'All in One' else None)
        if form.is_valid():
            # Save service manually because CreateNewService is a regular Form
            Service.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_per_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
                company=company
            )
            return redirect('company_profile', name=request.user.username)
    else:
        form = CreateNewService(choices=[(company.field, company.field)] if company.field != 'All in One' else None)

    return render(request, 'services/create_service.html', {'form': form})

# ------------------------------------------------------------------------
# Services filtered by field/category
# ------------------------------------------------------------------------
def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})
