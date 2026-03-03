from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, ProfileForm

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