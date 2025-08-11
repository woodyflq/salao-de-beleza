from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('services/', views.service_list, name='service_list'),
    path('team/', views.team_list, name='team_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('report/', views.report_completed_services, name='report_completed_services'),
]