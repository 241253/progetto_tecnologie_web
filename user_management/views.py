from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user_management.forms import ProfileCreationForm, UserForm


def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileCreationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile_form.save()

            # username = user_form.cleaned_data.get('username')
            # password = user_form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = ProfileCreationForm()
    
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'user_management/user_create.html', context)