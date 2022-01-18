from .models import UserForm
from django import forms

class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = UserForm
        fields = ['username', 'password', 'confirmPassword', 'email']