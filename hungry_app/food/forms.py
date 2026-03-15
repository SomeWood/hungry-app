from django import forms
from .models import FoodEntry


class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['food_name', 'meal_type', 'calories', 'date']