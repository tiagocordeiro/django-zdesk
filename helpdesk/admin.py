from django.contrib import admin

from .models import Queue, Ticket


class QueueAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('submitter_name',
                    'submitter_phone',
                    'submitter_email',
                    'submitter_company',
                    'queue',
                    'status',
                    'priority')
    list_filter = ('queue', 'status', 'priority')
    exclude = ('active',)


admin.site.register(Queue, QueueAdmin)
admin.site.register(Ticket, TicketAdmin)
