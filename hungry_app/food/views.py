import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import FoodEntry
from .forms import FoodEntryForm


@login_required
def food_log(request):
    selected_date = request.GET.get('date')

    if selected_date:
        food_entries = FoodEntry.objects.filter(user=request.user, date=selected_date)
    else:
        selected_date = datetime.date.today()
        food_entries = FoodEntry.objects.filter(user=request.user, date=selected_date)

    total_calories = 0
    for entry in food_entries:
        total_calories += entry.calories

    context = {
        'food_entries': food_entries,
        'selected_date': selected_date,
        'total_calories': total_calories,
    }

    return render(request, 'food/food_log.html', context)


@login_required
def add_food_entry(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            food_entry = form.save(commit=False)
            food_entry.user = request.user
            food_entry.save()
            return redirect('food_log')
    else:
        form = FoodEntryForm()

    context = {
        'form': form,
    }

    return render(request, 'food/add_food_entry.html', context)


@login_required
def delete_food_entry(request, entry_id):
    food_entry = get_object_or_404(FoodEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        food_entry.delete()
        return redirect('food_log')

    context = {
        'food_entry': food_entry,
    }

    return render(request, 'food/delete_food_entry.html', context)