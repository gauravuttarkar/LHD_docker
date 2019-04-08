from .models import User
from django import forms

class PostForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'address', 'city', 'state', 'email', 'phone_number', 'password', 'date_of_birth')