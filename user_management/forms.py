from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from user_management.models import User

class UserCreationForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_id = 'user-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Registrati'))

    class Meta:
        model = User
        fields = ('email', 'username', 'nome', 'cognome', 'password')