from django import forms
# from django.contrib.auth.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserForm

# Create your forms here.

class NewUserForm(forms.ModelForm):

	class Meta:
		model = UserForm
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user