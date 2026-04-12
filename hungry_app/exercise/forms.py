from django import forms
from .models import ExerciseEntry


class ExerciseEntryForm(forms.ModelForm):
    class Meta:
        model = ExerciseEntry
        fields = ['exercise_name', 'calories', 'duration', 'date']