import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from exercise.models import ExerciseEntry
from food.models import FoodEntry
from weight.models import WeightEntry


def calculate_tdee(profile):
    """
    Computes TDEE using the Mifflin-St Jeor BMR formula.
    Returns None if profile data is incomplete.
    """
    if not (profile.birthdate and profile.sex and profile.height and profile.activity_level):
        return None

    today = datetime.date.today()
    age = today.year - profile.birthdate.year - (
        (today.month, today.day) < (profile.birthdate.month, profile.birthdate.day)
    )

    # Get most recent weight for BMR — weight is needed
    latest_weight = WeightEntry.objects.filter(user=profile.user).first()
    if not latest_weight:
        return None

    weight_kg = latest_weight.weight
    height_cm = profile.height

    if profile.sex == 'Male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Athlete': 1.9,
    }
    multiplier = multipliers.get(profile.activity_level, 1.2)
    return round(bmr * multiplier)


@login_required
def dashboard_view(request):
    selected_date = request.GET.get('date')

    if selected_date:
        try:
            selected_date = datetime.date.fromisoformat(selected_date)
        except ValueError:
            selected_date = datetime.date.today()
    else:
        selected_date = datetime.date.today()

    food_entries = FoodEntry.objects.filter(user=request.user, date=selected_date)
    exercise_entries = ExerciseEntry.objects.filter(user=request.user, date=selected_date)

    total_food_calories = sum(e.calories for e in food_entries)
    total_exercise_calories = sum(e.calories for e in exercise_entries)
    net_calories = total_food_calories - total_exercise_calories

    # Latest weight
    latest_weight = WeightEntry.objects.filter(user=request.user).first()

    # TDEE
    profile = request.user.profile
    tdee = calculate_tdee(profile)

    # Calorie balance vs TDEE
    calorie_balance = None
    if tdee is not None:
        calorie_balance = net_calories - tdee

    context = {
        'selected_date': selected_date,
        'food_entries': food_entries,
        'exercise_entries': exercise_entries,
        'total_food_calories': total_food_calories,
        'total_exercise_calories': total_exercise_calories,
        'net_calories': net_calories,
        'latest_weight': latest_weight,
        'tdee': tdee,
        'calorie_balance': calorie_balance,
    }

    return render(request, 'dashboard/dashboard.html', context)
