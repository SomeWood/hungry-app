import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import ExerciseEntry
from .forms import ExerciseEntryForm

@login_required
def exercise_log(request):
    selected_date = request.GET.get('date')

    if selected_date:
        exercise_entries = ExerciseEntry.objects.filter(user=request.user, date=selected_date)
    else:
        selected_date = datetime.date.today()
        exercise_entries = ExerciseEntry.objects.filter(user=request.user, date=selected_date)

    total_calories = 0
    for entry in exercise_entries:
        total_calories += entry.calories

    context = {
        'exercise_entries': exercise_entries,
        'selected_date': selected_date,
        'total_calories': total_calories,
    }

    return render(request, 'exercise/exercise_log.html', context)


@login_required
def add_exercise_entry(request):
    if request.method == 'POST':
        form = ExerciseEntryForm(request.POST)
        if form.is_valid():
            exercise_entry = form.save(commit=False)
            exercise_entry.user = request.user
            exercise_entry.save()
            return redirect('exercise_log')
    else:
        form = ExerciseEntryForm()

    context = {
        'form': form,
    }

    return render(request, 'exercise/add_exercise_entry.html', context)


@login_required
def delete_exercise_entry(request, entry_id):
    exercise_entry = get_object_or_404(ExerciseEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        exercise_entry.delete()
        return redirect('exercise_log')

    context = {
        'exercise_entry': exercise_entry,
    }

    return render(request, 'exercise/delete_exercise_entry.html', context)