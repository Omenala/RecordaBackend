from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Adding custom fields to the user model
    phone = models.CharField(max_length=15)
    role_in_the_company = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_expiration = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    # Set the email field as the username for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    email = models.EmailField(unique=True)  # Ensure email is unique for authentication

    def __str__(self):
        return self.email
