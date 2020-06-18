from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user_management.forms import UserCreationForm


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_management/user_create.html'
    success_url = reverse_lazy('home')