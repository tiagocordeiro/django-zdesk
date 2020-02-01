from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html',)


@login_required
def profile_edit(request):
    return render(request, 'core/profile.html')
