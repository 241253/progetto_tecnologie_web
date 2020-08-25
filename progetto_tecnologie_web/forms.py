from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True, label='Oggetto')
    message = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none; width: 500px; height: 200px'}), required=True, label='Messaggio')