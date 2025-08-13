from django.contrib import admin
from .models import Client, Service, TeamMember, Appointment

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(TeamMember)
admin.site.register(Appointment)