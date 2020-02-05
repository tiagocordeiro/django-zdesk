from django.contrib import admin

from .models import Queue, Ticket, QueueQuestion


class QueueQuestionInline(admin.StackedInline):
    model = QueueQuestion
    extra = 1
    exclude = ('order',)


class QueueAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    inlines = [
        QueueQuestionInline,
    ]


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
