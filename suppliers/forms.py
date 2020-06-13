from django import forms

from .models import (
    Purchase,
    PurchaseDetail,
    Supplier
)


class NewSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

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
                    'class': 'form-control'
                }
            ),
            'address': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ),
            'city': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            )
        }


class NewPurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        exclude = ('products', )

        widgets = {
            'supplier': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ),
            'date': forms.DateInput(
                attrs = {
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#reservationdate'
                }
            ),
            'remarks': forms.TextInput (
                attrs = {
                    'class': 'form-control'
                }
            )
        }


class NewPurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'
        # exclude = ('purchase', )

        widgets = {
            'product': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ), 
            'description': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'cost': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'quantity': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }


PurchaseDetailInlineFormSet = forms.inlineformset_factory(
    Purchase, 
    PurchaseDetail, 
    form=NewPurchaseDetailForm, 
    extra = 4
)