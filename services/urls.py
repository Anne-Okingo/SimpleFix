# services/urls.py
from django.urls import path
from . import views as v

urlpatterns = [
    # List all services
    path('', v.service_list, name='service_list'),

    # Company creates a new service
    path('create/', v.create_service, name='create_service'),

    # Single service detail page (also handles requests)
    path('<int:id>/', v.service_detail, name='service_detail'),

    # Services filtered by category/field
    path('field/<slug:field>/', v.service_field, name='service_field'),

    # Customer requests a service
    path('<int:id>/request/', v.request_service, name='request_service'),
]
