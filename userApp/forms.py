from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken. Please choose another one.")
        return email


class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("This email is already taken. Please choose another one.")
        return email


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"})
    )


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter new password"}),
        min_length=8,
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm new password"}),
        min_length=8,
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
