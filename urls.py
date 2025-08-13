from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),  # Nova linha
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),  # Nova linha
    path('team/', views.team_member_list, name='team_member_list'),
    path('team/create/', views.team_member_create, name='team_member_create'),  # Nova linha
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('report/', views.report_completed_services, name='report_completed_services'),
    path('ajax/client/', views.ajax_search_client, name='ajax_search_client'),
    path('ajax/service/', views.ajax_search_service, name='ajax_search_service'),
    path('ajax/team/', views.ajax_search_team, name='ajax_search_team'),
]