from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.ticket_crete, name='ticket_create'),
    path('create/new/', views.ticket_crete_step02, name='ticket_create_step02'),
    path('create/new/done/', views.public_ticket_create, name='public_ticket_create'),
    path('detail/', views.ticket_detail, name='ticket_detail'),
]
