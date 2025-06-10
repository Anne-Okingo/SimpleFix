from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    """Custom date input widget that uses HTML5 date picker"""
    input_type = 'date'

# Validates that the email isn't already registered.

def validate_email(value):
    """
    Validates that the email isn't already registered.
    Raises ValidationError if email exists in User model.
    """
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")