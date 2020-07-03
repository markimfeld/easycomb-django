from django import forms

from .models import Customer

class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ('status',)
        widgets = {
            'first_name': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'phone': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                    'min': '0'
                }
            ),
            'city': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ),
            'address': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            )
        }
