from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, FileInput

from .models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', ]

        widgets = {
            'avatar': FileInput(attrs={'class': 'dropify'})
        }


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
