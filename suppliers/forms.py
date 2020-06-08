from django import forms

from .models import (
    Purchase,
    PurchaseDetail
)

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
            'date': forms.TextInput(
                attrs = {
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#reservationdate'
                }
            ),
            'remarks': forms.Textarea (
                attrs = {
                    'class': 'form-control'
                }
            )
        }


class NewPurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

        widgets = {
            'product': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ), 
            'description': forms.Textarea(
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
    Purchase, PurchaseDetail, form=NewPurchaseDetailForm, extra = 4, can_delete = True
)