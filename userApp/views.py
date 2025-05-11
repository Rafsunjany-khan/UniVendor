from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required


from .forms import (
    CustomUserRegistrationForm,
    CustomUserLoginForm,
    UserProfileForm,
    PasswordResetForm,
    SetNewPasswordForm,
)
from .models import CustomUser
from .utils import send_password_reset_email, send_verification_email


def user_signup(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            messages.info(request, "We have sent you a verification email.")
            return redirect("login")
    else:
        form = CustomUserRegistrationForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if not user:
                messages.error(request, "Invalid email or password.")
            elif not user.is_verified:
                messages.error(request, "Your email is not verified yet.")
            else:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("profile")
    else:
        form = CustomUserLoginForm()
    return render(request, "userApp/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def user_dashboard(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=user)

    return render(request, "userApp/profile.html", {"form": form})


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect("login")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("signup")


def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
                send_password_reset_email(request, user)
                messages.info(request, "We have sent you an email with password reset instructions.")
                return redirect("login")
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = PasswordResetForm()
    return render(request, "userApp/forgot.html", {"form": form})


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session["password_reset_user_id"] = user.id
        return redirect("new-password")
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect("login")


def set_new_password(request):
    user_id = request.session.get("password_reset_user_id")
    if not user_id:
        messages.error(request, "Session expired or invalid access.")
        return redirect("login")

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect("login")

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            messages.success(request, "Password updated successfully. You can now log in.")
            return redirect("login")
    else:
        form = SetNewPasswordForm()
    return render(request, "userApp/new-password.html", {"form": form})
