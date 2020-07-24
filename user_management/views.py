from sqlite3 import OperationalError

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView
from user_management.forms import ProfileCreationForm, UserForm, UserUpdateForm

def login_redirect(request):
    if request.user.is_staff:
        return render(request, 'user_management/staff/staff_page.html')
    else:
        return render(request, 'home.html')

#USER VIEW
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileCreationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile_form.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = ProfileCreationForm()

    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'user_management/user/user_create.html', context)

@method_decorator(login_required, name='dispatch')
class UserPage(DetailView):
    context_object_name = 'user'
    queryset = User.objects.all()
    extra_context = {'profile':queryset[0].profile}
    template_name = 'user_management/user/user_page.html'

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    model = User
    template_name = 'user_management/user/user_update.html'
    success_url = reverse_lazy('user_update_complete')

def UserUpdateComplete(request):
    return render(request, 'user_management/user/user_update_complete.html')


#STAFF VIEW
@method_decorator(login_required, name='dispatch')
class StaffPage(DetailView):
    context_object_name = 'user'
    queryset = User.objects.all()
    extra_context = {'profile': queryset[0].profile}
    template_name = 'user_management/user/staff_page.html'