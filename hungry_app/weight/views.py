import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import WeightEntry
from .forms import WeightEntryForm


@login_required
def weight_log(request):
    entries = WeightEntry.objects.filter(user=request.user)
    latest = entries.first()  # ordered by -date so first = most recent
    today = datetime.date.today()

    context = {
        'entries': entries,
        'latest': latest,
        'today': today,
    }
    return render(request, 'weight/weight_log.html', context)


@login_required
def add_weight_entry(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('weight_log')
    else:
        form = WeightEntryForm(initial={'date': datetime.date.today()})

    return render(request, 'weight/add_weight_entry.html', {'form': form})


@login_required
def delete_weight_entry(request, entry_id):
    entry = get_object_or_404(WeightEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        entry.delete()
        return redirect('weight_log')

    return render(request, 'weight/delete_weight_entry.html', {'entry': entry})
