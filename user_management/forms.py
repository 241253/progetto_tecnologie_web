from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

from user_management.models import Profile


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('foto',)

    def clean_avatar(self):
        foto = self.cleaned_data['foto']

        try:
            w, h = get_image_dimensions(foto)

            #validate dimensions
            max_width = max_height = 1000
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = foto.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

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