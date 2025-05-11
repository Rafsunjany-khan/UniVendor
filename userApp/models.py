from django.contrib.auth.models import AbstractUser
from django.db import models
from userApp.managers import CustomUserManager  # Ensure correct import path

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    address_line_1 = models.CharField(null=True, blank=True, max_length=100)
    address_line_2 = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=20)
    postcode = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    mobile = models.CharField(null=True, blank=True, max_length=15)

    profile_picture = models.ImageField(null=True, blank=True, upload_to="user_profile")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None

    objects = CustomUserManager()

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"

    # Override the groups field and add a related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Add related_name to avoid conflict
        blank=True,
    )

    # Optionally override permissions field as well
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Add related_name here too
        blank=True,
    )
