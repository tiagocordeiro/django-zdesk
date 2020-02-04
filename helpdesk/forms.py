from django import forms


class PublicTicketForm(forms.Form):
    """
    Ticket Form creation for all users (public-facing).
    """
    submitter_email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
        required=True,
        label=_('Your E-Mail Address'),
        help_text=_('We will e-mail you when your ticket is updated.'),
    )
