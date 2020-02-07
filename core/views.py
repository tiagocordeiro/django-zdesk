from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from core.forms import ProfileForm
from core.models import UserProfile
from helpdesk.models import Ticket


@login_required
def dashboard(request):
    tickets = Ticket.objects.all().exclude(status__in=[3, 4])
    tickets_resolved = Ticket.objects.filter(status=3)
    tickets_closed = Ticket.objects.filter(status=4)
    tickets_all = Ticket.objects.all()
    count_tickets_all = len(tickets_all)
    count_tickets_todo = len(tickets)
    count_tickets_resolved = len(tickets_resolved)
    count_tickets_closed = len(tickets_closed)
    context = {
        'tickets': tickets,
        'count_tickets_all': count_tickets_all,
        'count_tickets_todo': count_tickets_todo,
        'count_tickets_resolved': count_tickets_resolved,
        'count_tickets_closed': count_tickets_closed,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_edit(request):
    profile_inline_formset = inlineformset_factory(User, UserProfile, fields=('avatar',), extra=0, can_delete=False,
                                                   min_num=1, max_num=1, validate_min=True, validate_max=True)

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        formset = profile_inline_formset(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            perfil = form.save(commit=False)
            formset = profile_inline_formset(request.POST, request.FILES, instance=perfil)

            if formset.is_valid():
                perfil.save()
                formset.save()
                return redirect('profile_edit')

    else:
        form = ProfileForm(instance=request.user)
        formset = profile_inline_formset(instance=request.user)

    return render(request, 'core/profile.html', {'form': form,
                                                 'formset': formset, })
