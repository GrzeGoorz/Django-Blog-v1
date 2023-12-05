from django import forms
from django.core.exceptions import ValidationError
from .models import Item


class DateInput(forms.DateInput):
    input_type = 'date'
    

# ----------------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['product_name', 'quantity', 'location_name']

    product_name = forms.CharField(
        error_messages={
            'required': 'To pole nie może być puste.',
            'invalid': 'Wprowadź poprawne litery.',
        }
    )

    quantity = forms.IntegerField(
        error_messages={
            'required': 'To pole nie może być puste.',
            'invalid': 'Wprowadź poprawne cyfry.',
        }
    )