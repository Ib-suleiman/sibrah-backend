# ── forms.py ──────────────────────────────────────────────
from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model   = Enrollment
        fields  = ['schedule']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-select'}),
        }
