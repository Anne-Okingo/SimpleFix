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
        form = CreateNewService(request.POST, company=company)
        if form.is_valid():
            Service.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_per_hour=form.cleaned_data['price_per_hour'],
                field=form.cleaned_data['field'],
                company=company
            )
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
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import logging
from django.conf import settings
from django.contrib import messages

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from users.models import Company, Customer, User
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    """Public view - anyone can see service listings"""
    logger.debug("Entering service_list view")
    
    try:
        services = Service.objects.all().order_by('-date')
        logger.debug(f"Found {services.count()} total services")
        
        paginator = Paginator(services, 9)
        page = request.GET.get('page')
        services = paginator.get_page(page)
        
        context = {
            'services': services,
            'debug': True
        }
        
        return render(request, 'services/list.html', context)
        
    except Exception as e:
        logger.error(f"Error in service_list: {str(e)}")
        logger.exception("Full traceback:")
        raise


def index(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    """Protected view - only logged in companies can create services"""
    logger.debug("Entering create service view")
    
    # Check if user is a company
    if not hasattr(request.user, 'company'):
        messages.error(request, "Only companies can create services")
        return redirect('service_list')
        
    if request.method == 'POST':
        form = CreateNewService(request.POST)
        company = request.user.company
        if form.is_valid():
            if company.field != 'All in One' and company.field != form.cleaned_data['field']:
                form.add_error('field', 'You can only create services in your field of work.')
                return render(request, 'services/create.html', {'form': form})
            
            service = Service(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
            )
            service.save()
            return redirect('services_list')
    else:
        form = CreateNewService()
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})

@login_required
def request_service(request, id):
    """Protected view - only logged in customers can request services"""
    if not (request.user.is_authenticated and hasattr(request.user, 'customer')):
        messages.error(request, "Only logged in customers can request services")
        return redirect('service_list')
    
    try:
        service = get_object_or_404(Service, id=id)
        
        if request.method == 'POST':
            form = RequestServiceForm(request.POST)
            if form.is_valid():
                # Create service request
                ServiceRequest.objects.create(
                    service=service,
                    customer=request.user.customer,
                    address=form.cleaned_data['address'],
                    hours_needed=form.cleaned_data['hours_needed']
                )
                
                # Increment request count
                service.request_count += 1
                service.save()
                
                messages.success(request, f"Service request for {service.name} has been submitted")
                return redirect('services_list')
        else:
            form = RequestServiceForm()
            
        return render(request, 'services/request_service.html', {
            'form': form,
            'service': service
        })
        
    except Exception as e:
        logger.error(f"Error in request_service: {str(e)}")
        messages.error(request, "An error occurred while processing your request")
        return redirect('services_list')