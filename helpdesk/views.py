from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Queue, Ticket, QueueQuestion


def ticket_crete(request):
    queues = Queue.objects.all()
    return render(request, 'helpdesk/create_ticket_step01.html', {'queues': queues})


def ticket_crete_step02(request):
    queue = request.POST['maquina']
    queue = Queue.objects.get(title__exact=queue)
    questions = QueueQuestion.objects.filter(queue=queue)
    context = {
        'queue': queue,
        'questions': questions,
    }
    return render(request, 'helpdesk/create_ticket_step02.html', context)


def public_ticket_create(request):
    queue = request.POST['queue']
    problemas = request.POST.getlist('problemas')

    if 'Outros' in problemas:
        outros = request.POST['outros problemas']
        problemas.remove('Outros')
        problemas.append(outros)
    else:
        outros = None

    if request.method == 'POST':
        queue = Queue.objects.get(title__exact=queue)
        name = request.POST.get('nome')
        company = request.POST.get('empresa')
        mobile = request.POST.get('whats')
        email = request.POST.get('email')
        if request.POST.get('cliente') == 'on':
            is_customer = True
        else:
            is_customer = False

        new_ticket = Ticket.objects.create(queue=queue,
                                           problems=problemas,
                                           submitter_name=name,
                                           submitter_company=company,
                                           submitter_phone=mobile,
                                           submitter_email=email,
                                           is_customer=is_customer, )
        new_ticket.save()

    context = {
        'queue': queue,
        'problemas': problemas,
        'outros': outros
    }
    return render(request, 'helpdesk/create_ticket_done.html', context)


def ticket_detail(request, email, secret):
    ticket = Ticket.objects.get(secret_key=secret, submitter_email=email)
    return render(request, 'helpdesk/ticket_detail.html', {'ticket': ticket})


@login_required
def ticket_edit(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    return render(request, 'helpdesk/ticket_edit.html', {'ticket': ticket})
