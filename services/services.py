from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_per_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)  # get custom choices safely
        super().__init__(*args, **kwargs)
        if choices:
            self.fields['field'].choices = choices

        # adding placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_per_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'


class RequestServiceForm(forms.Form):
    pass
