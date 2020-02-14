from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from core.facade import get_dashboard_context
from core.forms import ProfileForm
from core.models import UserProfile


@login_required
def dashboard(request):
    context = get_dashboard_context()
    return render(request, 'core/dashboard.html', context)


@login_required
def live_dashboard(request):
    context = get_dashboard_context()
    return render(request, 'core/live-dashboard.html', context)


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
