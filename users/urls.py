from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.register, name='register'),
    path('company/', v.CompanySignUpView.as_view(), name='register_company'),
    path('customer/', v.CustomerSignUpView.as_view(), name='register_customer'),

    path('login/', v.LoginUserView, name='login'),
    path('logout/', v.logout_view, name='logout'),

    path('customer/<slug:name>/', v.customer_profile, name='customer_profile'),
    path('company/<slug:name>/', v.company_profile, name='company_profile'),
]
