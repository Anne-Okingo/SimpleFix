from django.urls import path
from . import views as v

urlpatterns = [
    # List all services
    path('', v.service_list, name='service_list'),

    # Company creates a new service
    path('create/', v.create_service, name='create_service'),

    # Single service detail page
    path('<int:id>/', v.service_detail, name='service_detail'),

    # Request a service (optional, also handled in service_detail)
    path('<int:id>/request/', v.request_service, name='request_service'),

    # Services filtered by category/field
    path('field/<slug:field>/', v.service_field, name='service_field'),
]
