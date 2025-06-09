from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(
        max_length=40,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Service name is required',
            'min_length': 'Service name must be at least 3 characters long',
            'max_length': 'Service name cannot exceed 40 characters'
        }
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        min_length=10,
        required=True,
        label='Description',
        error_messages={
            'required': 'Service description is required',
            'min_length': 'Description must be at least 10 characters long'
        }
    )
    price_hour = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        min_value=0.01,
        max_value=999.99,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Price per hour is required',
            'min_value': 'Price must be greater than 0',
            'max_value': 'Price cannot exceed 999.99',
            'invalid': 'Please enter a valid price'
        }
    )
    field = forms.ChoiceField(
        choices=(
            ('Air Conditioner', 'Air Conditioner'),
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
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Please select a service field',
            'invalid_choice': 'Please select a valid service field'
        }
    )
    def __init__(self, *args, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Remove extra whitespace
            name = ' '.join(name.split())
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            # Remove extra whitespace but preserve paragraphs
            description = '\n'.join(' '.join(p.split()) for p in description.split('\n') if p.strip())
        return description


class RequestServiceForm(forms.Form):
    pass
