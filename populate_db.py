import os
import django
import time
import sys
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_salon.settings")
django.setup()

import random
from faker import Faker
from django.utils import timezone
from salon.models import Client, Service, TeamMember, Appointment

fake = Faker('pt_BR')

def print_progress_bar(current, total, start_time):
    percent = (current / total) * 100
    elapsed_time = time.time() - start_time
    items_per_second = current / elapsed_time if elapsed_time > 0 else 1
    remaining_items = total - current
    estimated_remaining = remaining_items / items_per_second if items_per_second > 0 else 0
    eta = timedelta(seconds=int(estimated_remaining))

    bar_length = 50
    filled_length = int(bar_length * current // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write(f'\rProgresso: [{bar}] {percent:.1f}% ({current}/{total}) - ETA: {eta}')
    sys.stdout.flush()

def populate_database():
    start_time = time.time()
    total_clients = 2500
    total_appointments = 200

    print("Iniciando a população do banco de dados...")

    print(f"Criando {total_clients} clientes...")
    for i in range(total_clients):
        base_email = fake.email().split('@')[0]
        unique_email = f"{base_email}_{i:04d}@example.com"
        Client.objects.create(
            name=fake.name(),
            email=unique_email,
            phone=fake.phone_number()
        )
        print_progress_bar(i + 1, total_clients, start_time)
    print("\nClientes criados com sucesso!")

    print("Criando 15 serviços...")
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
    for i, (name, duration_str, price) in enumerate(services_data, 1):
        hours, minutes, seconds = map(int, duration_str.split(':'))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        Service.objects.create(name=name, duration=duration, price=price)
        print_progress_bar(i, len(services_data), start_time)
    print("\nServiços criados com sucesso!")

    print("Criando 15 membros da equipe...")
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
    for i, (name, specialty) in enumerate(team_members, 1):
        TeamMember.objects.create(name=name, specialty=specialty)
        print_progress_bar(i, len(team_members), start_time)
    print("\nMembros da equipe criados com sucesso!")

    print(f"Criando {total_appointments} agendamentos...")
    clients = Client.objects.all()
    services = Service.objects.all()
    team_members = TeamMember.objects.all()
    for i in range(total_appointments):
        appointment_time = fake.date_time_between(start_date="-30d", end_date="now",
                                                  tzinfo=timezone.get_current_timezone())
        status = random.choice(['SCHEDULED', 'COMPLETED', 'CANCELLED'])
        Appointment.objects.create(
            client=random.choice(clients),
            service=random.choice(services),
            team_member=random.choice(team_members),
            appointment_time=appointment_time,
            status=status
        )
        print_progress_bar(i + 1, total_appointments, start_time)
    print("\nAgendamentos criados com sucesso!")

    total_time = time.time() - start_time
    print(f"\nBanco de dados populado com sucesso! Tempo total: {timedelta(seconds=int(total_time))}")


if __name__ == "__main__":
    populate_database()