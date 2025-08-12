from django import forms
from .models import Client, Service, TeamMember, Appointment
from datetime import datetime

class AppointmentForm(forms.ModelForm):
    client = forms.CharField(label="Cliente", max_length=255, widget=forms.TextInput(attrs={'id': 'client-search', 'class': 'w-full px-4 py-2 border rounded-lg', 'data-id': ''}))
    service = forms.ChoiceField(label="Serviço", choices=[(s.id, s.name) for s in Service.objects.all()[:100]])
    team_member = forms.ChoiceField(label="Membro da Equipe", choices=[(tm.id, tm.name) for tm in TeamMember.objects.all()[:100]])

    class Meta:
        model = Appointment
        fields = ['client', 'service', 'team_member', 'appointment_time', 'status']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'service': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'team_member': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define a data e hora atual como padrão, sem segundos
        current_datetime = datetime.now().replace(microsecond=0).strftime('%Y-%m-%dT%H:%M')
        self.fields['appointment_time'].initial = current_datetime
        self.fields['appointment_time'].required = True
        # Limita as opções iniciais
        self.fields['service'].choices = [(s.id, s.name) for s in Service.objects.all()[:100]]
        self.fields['team_member'].choices = [(tm.id, tm.name) for tm in TeamMember.objects.all()[:100]]

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['client_id'] = self.data.get('client_id')
        cleaned_data['service_id'] = self.data.get('service_id')
        cleaned_data['team_member_id'] = self.data.get('team_member_id')
        return cleaned_data

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'duration', 'price']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'specialty']