from django import forms
from .models import CustomUser


# User Registration Form
class CustomUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'address_line_1', 'address_line_2',
            'city', 'postcode', 'country', 'mobile', 'profile_picture'
        ]

    # Define additional fields and validation
    email = forms.EmailField(required=True)
    address_line_1 = forms.CharField(max_length=255, required=True)
    address_line_2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=True)
    postcode = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=255, required=True)
    mobile = forms.CharField(max_length=20, required=True)
    profile_picture = forms.ImageField(required=False)


# User Login Form (Assuming it exists based on your `views.py` code)
class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


# Password Reset Form (for forgot password page)
class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True)


# Set New Password Form (for password reset confirmation)
class SetNewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# User Profile Update Form (for updating user profile)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'address_line_1', 'address_line_2', 'city', 'postcode', 'country', 'mobile', 'profile_picture'
        ]

    # Define additional fields and validation for profile updates
    address_line_1 = forms.CharField(max_length=255, required=True)
    address_line_2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=True)
    postcode = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=255, required=True)
    mobile = forms.CharField(max_length=20, required=True)
    profile_picture = forms.ImageField(required=False)
