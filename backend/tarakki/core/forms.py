# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)