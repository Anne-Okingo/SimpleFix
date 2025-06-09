from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from users.models import Company, Customer, User

from .models import Service
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
    service = Service.objects.get(id=id)
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
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    return render(request, 'services/request_service.html', {})
