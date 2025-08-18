from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


# ------------------------------------------------------------
# Reusable date input widget
# ------------------------------------------------------------
class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # Validators can be plugged into form fields
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")


# ------------------------------------------------------------
# 1) Customer Registration Form
# ------------------------------------------------------------
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    date_of_birth = forms.DateField(widget=DateInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Customer.objects.create(user=user, date_of_birth=self.cleaned_data["date_of_birth"])
        return user


# ------------------------------------------------------------
# 2) Company Registration Form
# ------------------------------------------------------------
class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    field = forms.ChoiceField(choices=Company._meta.get_field("field").choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Company.objects.create(user=user, field=self.cleaned_data["field"])
        return user


# ------------------------------------------------------------
# 3) Login form (email + password)
# ------------------------------------------------------------
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # turn off browser suggestions/autofill on email and password inputs
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['autocomplete'] = 'off'

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
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
        birth_date = self.cleaned_data.get('birth')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError('Birth date cannot be in the future.')
        return birth_date

    @transaction.atomic
    def save(self):
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
            ('Carpentry', 'Carpentry'),
            ('Electricity', 'Electricity'),
            ('Gardening', 'Gardening'),
            ('Home Machines', 'Home Machines'),
            ('Housekeeping', 'Housekeeping'),
            ('Interior Design', 'Interior Design'),
            ('Locks', 'Locks'),
            ('Painting', 'Painting'),
            ('Plumbing', 'Plumbing'),
            ('Water Heaters', 'Water Heaters')
        ),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your field of work'
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
        fields = ('username', 'email', 'password1', 'password2', 'field')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        user.save()
        company = Company.objects.create(
            user=user,
            field=self.cleaned_data.get('field')
        )
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
