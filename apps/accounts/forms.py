"""
SIBRAH Accounts App — Forms
apps/accounts/forms.py
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SibrahUser


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
    phone = forms.CharField(
        max_length=20, required=True,
        widget=forms.TextInput(attrs={'placeholder': '+234...'})
    )

    class Meta:
        model  = SibrahUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.phone      = self.cleaned_data['phone']
        user.role       = 'student'
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model  = SibrahUser
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'address', 'date_of_birth', 'profile_pic')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address':       forms.Textarea(attrs={'rows': 3}),
        }
