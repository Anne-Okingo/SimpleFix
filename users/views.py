from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer

from services.models import ServiceRequest


def register(request):
    return render(request, 'users/register.html')


# ------------------------------------------------------------
# Registration (class-based views)
# ------------------------------------------------------------

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer_profile', name=user.username)


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('company_profile', name=user.username)


# ------------------------------------------------------------
# Login View
# ------------------------------------------------------------

def LoginUserView(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                user_obj = None

            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_customer:
                        return redirect('customer_profile', name=user.username)
                    if user.is_company:
                        return redirect('company_profile', name=user.username)
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'users/login.html', {'form': form})


# ------------------------------------------------------------
# Logout View
# ------------------------------------------------------------

def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------------------------------------------------
# Profile views (simple examples)
# ------------------------------------------------------------

def customer_profile(request, name):
    # Get the customer object
    customer = Customer.objects.get(user__username=name)
    # Get all service requests by this customer, newest first
    requested_services = ServiceRequest.objects.filter(customer=customer).order_by('-requested_at')
    
    return render(request, 'users/profile_customer.html', {
        'customer': customer,
        'requested_services': requested_services
    })


def company_profile(request, name):
    # Get the company object
    company = Company.objects.get(user__username=name)
    # Get all services offered by this company, newest first
    services = company.service_set.all().order_by('-created_at')
    
    return render(request, 'users/profile_company.html', {
        'company': company,
        'services': services
    })
