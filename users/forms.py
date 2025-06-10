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


class CustomerSignUpForm(UserCreationForm):
    
    # Form field definitions with custom widgets and attributes
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    birth = forms.DateField(
        required=True,
        widget=DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select your date of birth'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth')
    
    def clean_birth(self):
        """Validate that birth date isn't in the future"""
        birth_date = self.cleaned_data.get('birth')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError('Birth date cannot be in the future.')
        return birth_date

    @transaction.atomic
    def save(self):
        """
        Saves the user as a customer with atomic transaction:
        1. Creates User with is_customer=True
        2. Creates associated Customer profile
        """
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(
            user=user,
            birth=self.cleaned_data.get('birth')
        )
        return user       


class CompanySignUpForm(UserCreationForm):
    """
    Form for company registration with:
    - Company name (as username)
    - Email (with validation)
    - Field of work selection
    - Password fields
    """
    
    # Form field definitions
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your company name'
        })
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter company email address'
        })
    )
    field = forms.ChoiceField(
        choices=(
            ('Air Conditioner', 'Air Conditioner'),
            ('All in One', 'All in One'),
            # ... other choices ...
            ('Water Heaters', 'Water Heaters')
        ),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your field of work'
        })
    )
    # Password fields same as CustomerSignUpForm...

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'field')

    @transaction.atomic
    def save(self):
        """
        Saves the user as a company with atomic transaction:
        1. Creates User with is_company=True
        2. Creates associated Company profile
        """
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        user.save()
        company = Company.objects.create(
            user=user,
            field=self.cleaned_data.get('field')
        )
        return user