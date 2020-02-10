from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import TicketManageForm, TicketForm
from .models import Queue, Ticket, QueueQuestion, TicketUpdate


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


def load_questions(request):
    queue = request.GET.get('queue')
    questions = QueueQuestion.objects.filter(queue=queue)
    return render(request, 'helpdesk/questions_builder.html', {'questions': questions})


@login_required
def ticket_add(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            new_ticket = form.save(commit=False)

            if 'Outros' in form.data.getlist('problems'):
                problems = form.data.getlist('problems')
                outros = form.data.get('outros problemas')

                problems.remove('Outros')
                problems.append(outros)
            else:
                problems = form.data.getlist('problems')

            new_ticket.problems = problems
            new_ticket.assigned_to = new_ticket.tecnico_pre_diagnostico = request.user

            new_ticket.save()
            messages.success(request, "Novo ticket cadastrado")
            return redirect('ticket_edit', pk=new_ticket.pk)

    else:
        form = TicketForm()

    context = {
        'form': form,
    }
    return render(request, 'helpdesk/ticket_add.html', context)


@login_required
def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        form = TicketManageForm(request.POST, request.FILES, instance=ticket)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "O ticket foi atualizado")
                return redirect(ticket_edit, pk=pk)

        except Exception as e:
            messages.warning(request, 'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = TicketManageForm(instance=ticket)

    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'helpdesk/ticket_edit.html', context)


@login_required
def ticket_list_all(request):
    tickets = Ticket.objects.all()
    context = {
        'tickets': tickets,
        'title': 'Todos os tickets',
        'table_title': 'Todos os<strong> Tickets</strong>',
        'breadcrumb': 'Todos',
    }
    return render(request, 'helpdesk/ticket_list.html', context)


@login_required
def ticket_list_todo(request):
    tickets = Ticket.objects.all().exclude(status__in=[3, 4])
    context = {
        'tickets': tickets,
        'title': 'Tickets para fazer',
        'table_title': '<strong>Tickets </strong>para fazer',
        'breadcrumb': 'Para fazer',
    }
    return render(request, 'helpdesk/ticket_list.html', context)


@login_required
def ticket_list_done(request):
    tickets = Ticket.objects.filter(status__in=[3, 4])
    context = {
        'tickets': tickets,
        'title': 'Tickets feitos',
        'table_title': '<strong>Tickets </strong>feitos',
        'breadcrumb': 'Feitos',
    }
    return render(request, 'helpdesk/ticket_list.html', context)


@login_required
def ticket_comment(request, **kwargs):
    ticket = Ticket.objects.get(pk=request.POST.get('update_ticket_pk'))
    user = request.user
    title = request.POST.get('update_title')
    comment = request.POST.get('update_comment')
    TicketUpdate.objects.create(ticket=ticket, user=user, title=title, comment=comment, public=False)

    messages.success(request, "Novo comentário adicionado")
    return redirect(reverse('ticket_edit', args={ticket.pk}))
