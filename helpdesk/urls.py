from django.urls import path

from . import views

urlpatterns = [
    path('ticket/create/', views.ticket_crete, name='ticket_create'),
    path('ticket/create/new/', views.ticket_crete_step02, name='ticket_create_step02'),
    path('ticket/create/new/done/', views.public_ticket_create, name='public_ticket_create'),
    path('ticket/<email>/<secret>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<pk>/', views.ticket_edit, name='ticket_edit'),
    path('tickets/', views.ticket_list_all, name='ticket_list_all'),
    path('tickets/todo/', views.ticket_list_todo, name='ticket_list_todo'),
    path('tickets/done/', views.ticket_list_done, name='ticket_list_done'),
]
