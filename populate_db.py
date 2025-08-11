import os
import django

# Configura o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_salon.settings")
django.setup()

import random
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from salon.models import Client, Service, TeamMember, Appointment

fake = Faker('pt_BR')  # Gera dados em português brasileiro

# Função para criar dados fictícios
def populate_database():
    # Criar clientes
    for _ in range(100):  # 10 clientes
        Client.objects.create(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )

    # Criar serviços
    services_data = [
        ("Corte de Cabelo", "01:00:00", 50.00),
        ("Manicure", "00:45:00", 30.00),
        ("Pedicure", "01:00:00", 40.00),
        ("Coloração", "02:00:00", 80.00),
        ("Hidratação", "01:30:00", 60.00),
    ]
    for name, duration_str, price in services_data:
        # Converter string de duração para timedelta
        hours, minutes, seconds = map(int, duration_str.split(':'))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        Service.objects.create(name=name, duration=duration, price=price)

    # Criar membros da equipe
    team_members = [
        ("Ana Silva", "Cabelereira"),
        ("Maria Clara", "Manicure"),
        ("Maria Oliveira", "Esteticista"),
        ("Carlos Souza", "Barbeiro"),
        ("Pedro Jorge", "Barbeiro")
    ]
    for name, specialty in team_members:
        TeamMember.objects.create(name=name, specialty=specialty)

    # Criar agendamentos
    clients = Client.objects.all()
    services = Service.objects.all()
    team_members = TeamMember.objects.all()
    for _ in range(200):  # 20 agendamentos
        appointment_time = fake.date_time_between(start_date="-30d", end_date="now", tzinfo=timezone.get_current_timezone())
        status = random.choice(['SCHEDULED', 'COMPLETED', 'CANCELLED'])
        Appointment.objects.create(
            client=random.choice(clients),
            service=random.choice(services),
            team_member=random.choice(team_members),
            appointment_time=appointment_time,
            status=status
        )

    print("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    populate_database()