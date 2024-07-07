from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    phone_number = forms.CharField(max_length=15, required=False, help_text='Optional. Enter your phone number.')
    address = forms.CharField(max_length=255, required=False, help_text='Optional. Enter your address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.address = self.cleaned_data.get('address')
        if commit:
            user.save()
        return user
