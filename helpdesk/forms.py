from django.forms import ModelForm, Select, CheckboxInput, Textarea, TextInput, EmailInput, CheckboxSelectMultiple

from .models import Ticket


class TicketManageForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['status',
                  'priority',
                  'tecnico_pre_diagnostico',
                  'tecnico_de_campo',
                  'is_customer',
                  'customer_code',
                  'order',
                  'need_paper',
                  'resolution_report', ]

        widgets = {
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'priority': Select(attrs={'class': 'form-control', 'placeholder': 'Prioridade'}),
            'tecnico_pre_diagnostico': Select(attrs={'class': 'form-control', 'placeholder': 'Pré diagnostico'}),
            'tecnico_de_campo': Select(attrs={'class': 'form-control', 'placeholder': 'Tecnico de campo'}),
            'is_customer': CheckboxInput(attrs={'class': 'form-control'}),
            'customer_code': TextInput(attrs={'class': 'form-control'}),
            'order': TextInput(attrs={'class': 'form-control'}),
            'need_paper': CheckboxInput(attrs={'class': 'form-control'}),
            'resolution_report': Textarea(attrs={'class': 'form-control'})
        }


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['queue',
                  'problems',
                  'submitter_name',
                  'submitter_company',
                  'submitter_phone',
                  'submitter_email',
                  'status',
                  'priority',
                  'tecnico_pre_diagnostico',
                  'tecnico_de_campo',
                  'is_customer',
                  'customer_code',
                  'order',
                  'need_paper',
                  'resolution_report', ]

        widgets = {
            'queue': Select(attrs={'class': 'form-control', 'placeholder': 'Queue'}),
            'problems': CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'submitter_name': TextInput(attrs={'class': 'form-control'}),
            'submitter_company': TextInput(attrs={'class': 'form-control'}),
            'submitter_phone': TextInput(attrs={'class': 'form-control'}),
            'submitter_email': EmailInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'priority': Select(attrs={'class': 'form-control', 'placeholder': 'Prioridade'}),
            'tecnico_pre_diagnostico': Select(attrs={'class': 'form-control', 'placeholder': 'Pré diagnostico'}),
            'tecnico_de_campo': Select(attrs={'class': 'form-control', 'placeholder': 'Tecnico de campo'}),
            'is_customer': CheckboxInput(attrs={'class': 'form-control'}),
            'customer_code': TextInput(attrs={'class': 'form-control'}),
            'order': TextInput(attrs={'class': 'form-control'}),
            'need_paper': CheckboxInput(attrs={'class': 'form-control'}),
            'resolution_report': Textarea(attrs={'class': 'form-control'})
        }
