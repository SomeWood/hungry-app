import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from exercise.models import ExerciseEntry
from food.models import FoodEntry

# Create your views here.
@login_required
def dashboard_view(request):
    selected_date = request.GET.get('date')

    if selected_date:
        food_entries = FoodEntry.objects.filter(user=request.user, date=selected_date)
        exercise_entries = ExerciseEntry.objects.filter(user=request.user, date=selected_date)
    else:
        selected_date = datetime.date.today()
        food_entries = FoodEntry.objects.filter(user=request.user, date=selected_date)
        exercise_entries = ExerciseEntry.objects.filter(user=request.user, date=selected_date)

    total_calories = 0
    for entry in food_entries:
        total_calories += entry.calories
    for entry in exercise_entries:
        total_calories -= entry.calories

    context = {'total_calories' : total_calories}

    return render(request, 'dashboard/dashboard.html', context)