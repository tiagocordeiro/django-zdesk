from django.forms import ModelForm, Select, CheckboxInput, Textarea, TextInput

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
                  'need_paper',
                  'resolution_report', ]

        widgets = {
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'priority': Select(attrs={'class': 'form-control', 'placeholder': 'Prioridade'}),
            'tecnico_pre_diagnostico': Select(attrs={'class': 'form-control', 'placeholder': 'Pré diagnostico'}),
            'tecnico_de_campo': Select(attrs={'class': 'form-control', 'placeholder': 'Tecnico de campo'}),
            'is_customer': CheckboxInput(attrs={'class': 'form-control'}),
            'customer_code': TextInput(attrs={'class': 'form-control'}),
            'need_paper': CheckboxInput(attrs={'class': 'form-control'}),
            'resolution_report': Textarea(attrs={'class': 'form-control'})
        }
