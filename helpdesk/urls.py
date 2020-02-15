from django.urls import path

from . import views

urlpatterns = [
    path('ticket/add/', views.ticket_add, name='ticket_add'),
    path('ticket/create/', views.ticket_crete, name='ticket_create'),
    path('ticket/create/new/', views.ticket_crete_step02, name='ticket_create_step02'),
    path('ticket/create/new/done/', views.public_ticket_create, name='public_ticket_create'),
    path('ticket/<email>/<secret>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<pk>/', views.ticket_edit, name='ticket_edit'),
    path('tickets/', views.ticket_list_all, name='ticket_list_all'),
    path('tickets/todo/', views.ticket_list_todo, name='ticket_list_todo'),
    path('tickets/done/', views.ticket_list_done, name='ticket_list_done'),
    path('tickets/processing/', views.ticket_list_processing, name='ticket_list_processing'),
    path('tickets/comment/<pk>/', views.ticket_comment, name='ticket_comment'),
    path('tickets/ajax/load-questions/', views.load_questions, name='load_questions'),
    path('tickets/ajax/feed/', views.ticket_feed, name='ticket_feed')
]
