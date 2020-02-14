from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('live/', views.live_dashboard, name='live_dashboard'),
    path('profile/', views.profile_edit, name='profile_edit'),
]
