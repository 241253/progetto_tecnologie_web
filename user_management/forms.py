from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from user_management.models import Profile

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = "Richiesti 150 caratteri o meno. Sono ammessi solo lettere, cifre e @/./+/-/_."
        self.fields['password1'].help_text = "<ul> <li> La tua password non può essere troppo simile alle tue informazioni personali.</li>" \
                                             "<li> La tua password deve contenere almeno 8 aratteri. </li>" \
                                             "<li> La tua password non può essere una password usata troppo comunemente. </li>" \
                                             "<li> La tua password non può essere solamente numerica. </li>" \
                                             "</ul>"
        self.fields['email'].label = "Indirizzo email"
        self.fields['email'].required = True
        self.fields['username'].label = "Username"
        self.fields['first_name'].label = "Nome"
        self.fields['first_name'].required = True
        self.fields['last_name'].label = "Cognome"
        self.fields['last_name'].required = True
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Ripeti password"
        self.error_messages['password_mismatch'] = "Le due password non combaciano."
        self.fields['password2'].help_text = "Ripeti la password, per motivi di sicurezza."

class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('foto',)

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)
        self.fields['foto'].label = "Foto"
        self.fields['foto'].required = False

    def clean_foto(self):
        foto = self.cleaned_data['foto']

        try:
            w, h = get_image_dimensions(foto)

            #validate dimensions
            max_width = max_height = 1500
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = foto.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')

            #validate file size
            if len(foto) > (4000 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 4MB.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return foto

#STAFF
class StaffForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = "Richiesti 150 caratteri o meno. Sono ammessi solo lettere, cifre e @/./+/-/_."
        self.fields['password1'].help_text = "<ul> <li> La tua password non può essere troppo simile alle tue informazioni personali.</li>" \
                                             "<li> La tua password deve contenere almeno 8 aratteri. </li>" \
                                             "<li> La tua password non può essere una password usata troppo comunemente. </li>" \
                                             "<li> La tua password non può essere solamente numerica. </li>" \
                                             "</ul>"
        self.fields['email'].label = "Indirizzo email"
        self.fields['email'].required = True
        self.fields['username'].label = "Username"
        self.fields['first_name'].label = "Nome"
        self.fields['first_name'].required = True
        self.fields['last_name'].label = "Cognome"
        self.fields['last_name'].required = True
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Ripeti password"
        self.error_messages['password_mismatch'] = "Le due password non combaciano."
        self.fields['password2'].help_text = "Ripeti la password, per motivi di sicurezza."

    def save(self, commit=True):
        user = super(StaffForm, self).save(commit=False)
        user.is_staff = True

        if commit:
            user.save()
        return user

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

        def __init__(self, *args, **kwargs):
            super(forms.ModelForm, self).__init__(*args, **kwargs)
            print("CIAO3")