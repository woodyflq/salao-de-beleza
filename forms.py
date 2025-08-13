from django import forms
from .models import Client, Service, TeamMember, Appointment
from datetime import datetime

class AppointmentForm(forms.ModelForm):
    client = forms.CharField(label="Cliente", max_length=255, widget=forms.TextInput(attrs={'id': 'client-search', 'class': 'w-full px-4 py-2 border rounded-lg', 'data-id': ''}))
    service = forms.ChoiceField(label="Serviço")
    team_member = forms.ChoiceField(label="Membro da Equipe")

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
        current_datetime = datetime.now().replace(microsecond=0).strftime('%Y-%m-%dT%H:%M')
        self.fields['appointment_time'].initial = current_datetime
        self.fields['appointment_time'].required = True
        self.fields['service'].choices = [('', 'Selecione um serviço')] + [(s.id, s.name) for s in Service.objects.all()[:100]]
        self.fields['team_member'].choices = [('', 'Selecione um membro')] + [(tm.id, tm.name) for tm in TeamMember.objects.all()[:100]]

    def clean(self):
        cleaned_data = super().clean()
        client_id = self.data.get('client_id')
        service_id = self.data.get('service')
        team_member_id = self.data.get('team_member')

        if client_id:
            try:
                cleaned_data['client'] = Client.objects.get(id=client_id)
            except Client.DoesNotExist:
                raise forms.ValidationError("Cliente selecionado não existe.")
        if service_id:
            try:
                cleaned_data['service'] = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                raise forms.ValidationError("Serviço selecionado não existe.")
        if team_member_id:
            try:
                cleaned_data['team_member'] = TeamMember.objects.get(id=team_member_id)
            except TeamMember.DoesNotExist:
                raise forms.ValidationError("Membro da equipe selecionado não existe.")

        return cleaned_data

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'duration', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'duration': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'HH:MM:SS'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class TeamMemberForm(forms.ModelForm):
    specialty = forms.ChoiceField(choices=[('', 'Selecione um serviço')], required=False, label="Especialidade")

    class Meta:
        model = TeamMember
        fields = ['name', 'specialty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'specialty': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_choices = [(s.id, s.name) for s in Service.objects.all()]
        self.fields['specialty'].choices = [('', 'Selecione um serviço')] + service_choices

    def clean_specialty(self):
        specialty = self.cleaned_data['specialty']
        if specialty and not Service.objects.filter(id=specialty).exists():
            raise forms.ValidationError(f"'{specialty}' não é uma escolha válida.")
        return specialty

    def save(self, *args, **kwargs):
        if self.cleaned_data['specialty']:
            service = Service.objects.get(id=self.cleaned_data['specialty'])
            self.instance.specialty = service.name
        return super().save(*args, **kwargs)