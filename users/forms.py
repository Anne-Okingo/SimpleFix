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

