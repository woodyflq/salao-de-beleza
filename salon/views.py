from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Client, Service, TeamMember, Appointment
from .forms import AppointmentForm
from datetime import datetime, date
from .forms import ClientForm, ServiceForm, TeamMemberForm  # Adiciona isso no topo, se não tiver


def paginate_queryset(request, queryset, default_page_size=10):
    page_size = request.GET.get('page_size', default_page_size)
    try:
        page_size = int(page_size)
    except ValueError:
        page_size = default_page_size
    if page_size not in [10, 20, 50]:
        page_size = default_page_size
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj, page_size


from django.db.models import Count  # Adiciona isso no topo, se não tiver

def client_list(request):
    clients = Client.objects.annotate(appointment_count=Count('appointment'))  # Calcula o número de agendamentos
    page_obj, page_size = paginate_queryset(request, clients)
    return render(request, 'client_list.html', {'page_obj': page_obj, 'page_size': page_size})


def service_list(request):
    services = Service.objects.all()
    page_obj, page_size = paginate_queryset(request, services)
    return render(request, 'service_list.html', {'page_obj': page_obj, 'page_size': page_size})


def team_list(request):
    team_members = TeamMember.objects.all()
    page_obj, page_size = paginate_queryset(request, team_members)
    return render(request, 'team_list.html', {'page_obj': page_obj, 'page_size': page_size})


def appointment_list(request):
    appointments = Appointment.objects.select_related('client', 'service', 'team_member').all()
    page_obj, page_size = paginate_queryset(request, appointments)
    return render(request, 'appointment_list.html', {'page_obj': page_obj, 'page_size': page_size})


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = Appointment.objects.create(
                client_id=form.cleaned_data['client_id'],
                service_id=form.cleaned_data['service_id'],
                team_member_id=form.cleaned_data['team_member_id'],
                appointment_time=form.cleaned_data['appointment_time'],
                status=form.cleaned_data['status']
            )
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})

def ajax_search_client(request):
    term = request.GET.get('term', '')
    clients = Client.objects.filter(name__icontains=term)[:10]
    results = [{'id': c.id, 'text': c.name} for c in clients]
    return JsonResponse({'results': results})

def ajax_search_service(request):
    pass

def ajax_search_team(request):
    pass

def report_completed_services(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = None
    end_date = None

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = date.today()  # Definir data final como atual por padrão

    appointments = Appointment.objects.filter(status='COMPLETED')

    if start_date and end_date:
        appointments = appointments.filter(
            appointment_time__range=[start_date, end_date]
        )

    report_data = appointments.values('service__name').annotate(total=Count('id')).order_by('service__name')

    return render(request, 'report.html', {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
    })

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_form.html', {'form': form})

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'service_form.html', {'form': form})

def team_member_create(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'team_member_form.html', {'form': form})