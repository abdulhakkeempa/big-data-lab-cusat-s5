from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from accounts.models import User

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')
