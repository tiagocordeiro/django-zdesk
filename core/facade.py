from helpdesk.models import Ticket


def get_dashboard_context():
    tickets = Ticket.objects.all().exclude(status__in=[3, 4, 5, 6])
    tickets_processing = Ticket.objects.filter(status=6)
    tickets_resolved = Ticket.objects.filter(status=3)
    tickets_closed = Ticket.objects.filter(status=4)
    tickets_all = Ticket.objects.all()
    count_tickets_all = len(tickets_all)
    count_tickets_todo = len(tickets)
    count_tickets_resolved = len(tickets_resolved)
    count_tickets_closed = len(tickets_closed)
    total_losses = 0
    for ticket in tickets_all:
        if ticket.losses:
            total_losses = ticket.losses + total_losses

    context = {
        'tickets': tickets,
        'count_tickets_all': count_tickets_all,
        'count_tickets_todo': count_tickets_todo,
        'count_tickets_resolved': count_tickets_resolved,
        'count_tickets_closed': count_tickets_closed,
        'tickets_processing': tickets_processing,
        'total_losses': total_losses
    }
    return context
