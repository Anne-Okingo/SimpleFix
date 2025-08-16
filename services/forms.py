from django import forms
from .models import Service
from users.models import Company

# -------------------------------------------------------------------------
# Service creation form for companies
# -------------------------------------------------------------------------
class CreateNewService(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price_per_hour', 'field']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Service Name'}),
            'price_per_hour': forms.NumberInput(attrs={'placeholder': 'Enter Price per Hour'}),
        }
        labels = {
            'price_per_hour': 'Price per Hour'
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        # Restrict field choices based on company type
        all_fields = [
            ('Air Conditioner', 'Air Conditioner'),
            ('All in One', 'All in One'),
            ('Carpentry', 'Carpentry'),
            ('Electricity', 'Electricity'),
            ('Gardening', 'Gardening'),
            ('Home Machines', 'Home Machines'),
            ('House Keeping', 'House Keeping'),
            ('Interior Design', 'Interior Design'),
            ('Locks', 'Locks'),
            ('Painting', 'Painting'),
            ('Plumbing', 'Plumbing'),
            ('Water Heaters', 'Water Heaters'),
        ]

        if company:
            if company.field == 'All in One':
                self.fields['field'].choices = [f for f in all_fields if f[0] != 'All in One']
            else:
                # Only allow company’s field
                self.fields['field'].choices = [(company.field, company.field)]
        else:
            self.fields['field'].choices = all_fields


class RequestServiceForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Address'})
    )
    hours = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Number of Hours'})
    )
