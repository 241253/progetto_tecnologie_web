from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User

from user_management.models import Profile


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('foto',)