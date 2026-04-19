import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileForm, ProfileEditForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = user.profile
            profile.birthdate = profile_form.cleaned_data['birthdate']
            profile.sex = profile_form.cleaned_data['sex']
            profile.height = profile_form.cleaned_data['height']
            profile.activity_level = profile_form.cleaned_data['activity_level']
            profile.save()

            login(request, user)
            return redirect('dashboard')

    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def profile_view(request):
    profile = request.user.profile

    # Compute age from birthdate if available
    age = None
    if profile.birthdate:
        today = datetime.date.today()
        age = today.year - profile.birthdate.year - (
            (today.month, today.day) < (profile.birthdate.month, profile.birthdate.day)
        )

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'profile': profile,
        'age': age,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)
