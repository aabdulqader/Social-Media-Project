from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):

    email = forms.EmailField(label=("Email"))

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2' )


        







