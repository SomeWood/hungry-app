from django import forms
from .models import WeightEntry


class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
