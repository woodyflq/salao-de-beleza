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
    # [1] Criar 5000 clientes com e-mails únicos
    for i in range(5000):
        # Adiciona um sufixo único baseado no índice
        base_email = fake.email().split('@')[0]  # Pega só a parte antes do @
        unique_email = f"{base_email}_{i:04d}@example.com"  # Ex.: nome_0001@example.com
        Client.objects.create(
            name=fake.name(),
            email=unique_email,
            phone=fake.phone_number()
        )

    # [2] Criar serviços (15 opções)
    services_data = [
        ("Corte de Cabelo", "01:00:00", 50.00),
        ("Manicure", "00:45:00", 30.00),
        ("Pedicure", "01:00:00", 40.00),
        ("Coloração", "02:00:00", 80.00),
        ("Hidratação", "01:30:00", 60.00),
        ("Maquiagem", "01:00:00", 70.00),
        ("Depilação", "00:30:00", 25.00),
        ("Massagem Relaxante", "01:00:00", 90.00),
        ("Escova Progressiva", "02:30:00", 150.00),
        ("Penteado", "00:45:00", 50.00),
        ("Tratamento Facial", "01:15:00", 80.00),
        ("Design de Sobrancelha", "00:30:00", 35.00),
        ("Alongamento de Unhas", "01:30:00", 60.00),
        ("Barba", "00:30:00", 30.00),
        ("Limpeza de Pele", "01:00:00", 70.00),
    ]
    for name, duration_str, price in services_data:
        # Converter string de duração para timedelta
        hours, minutes, seconds = map(int, duration_str.split(':'))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        Service.objects.create(name=name, duration=duration, price=price)

    # [3] Criar membros da equipe (máximo de 15 pessoas)
    team_members = [
        ("Ana Silva", "Cabelereira"),
        ("Maria Clara", "Manicure"),
        ("Maria Oliveira", "Esteticista"),
        ("Carlos Souza", "Barbeiro"),
        ("Pedro Jorge", "Barbeiro"),
        ("Juliana Mendes", "Cabelereira"),
        ("Lucas Ferreira", "Esteticista"),
        ("Fernanda Costa", "Manicure"),
        ("Rafael Almeida", "Barbeiro"),
        ("Sofia Ribeiro", "Cabelereira"),
        ("Gabriel Santos", "Esteticista"),
        ("Isabela Lima", "Manicure"),
        ("Matheus Oliveira", "Barbeiro"),
        ("Laura Pereira", "Cabelereira"),
        ("Enzo Rodrigues", "Esteticista"),
    ]
    for name, specialty in team_members:
        TeamMember.objects.create(name=name, specialty=specialty)

    # [4] Criar 200 agendamentos
    clients = Client.objects.all()
    services = Service.objects.all()
    team_members = TeamMember.objects.all()
    for _ in range(200):
        appointment_time = fake.date_time_between(start_date="-30d", end_date="now", tzinfo=timezone.get_current_timezone())
        status = random.choice(['SCHEDULED', 'COMPLETED', 'CANCELLED'])
        Appointment.objects.create(
            client=random.choice(clients),
            service=random.choice(services),
            team_member=random.choice(team_members),
            appointment_time=appointment_time,
            status=status
        )

    # [5] Mensagem de sucesso
    print("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    populate_database()