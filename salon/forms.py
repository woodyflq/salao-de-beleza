from django import forms
from .models import Client, Service, TeamMember, Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'service', 'team_member', 'appointment_time', 'status']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'duration', 'price']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),  # Pra ajudar no formato
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'specialty']