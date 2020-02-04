from django.shortcuts import render

from .models import Queue


def ticket_crete(request):
    queues = Queue.objects.all()
    return render(request, 'helpdesk/create_ticket_step01.html', {'queues': queues})


def ticket_crete_step02(request):
    queue = request.POST['maquina']
    context = {
        'queue': queue,
    }
    return render(request, 'helpdesk/create_ticket_step02.html', context)


def public_ticket_create(request):
    queue = request.POST['queue']
    problemas = request.POST.getlist('problemas')

    if 'Outros' in problemas:
        outros = request.POST['outros problemas']
    else:
        outros = None

    context = {
        'queue': queue,
        'problemas': problemas,
        'outros': outros
    }
    return render(request, 'helpdesk/create_ticket_done.html', context)


def ticket_detail(request):
    return render(request, 'helpdesk/ticket_detail.html')
