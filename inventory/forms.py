
from django import forms
from .models import (
    Product,
    Category,
    Combo,
    ComboDetail
)


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('stock',)
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'rows': '4'
                }
            ),
            'category': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ),
            'wholesale_price': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'retail_price': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs = {
                    'class': 'custom-file-input'
                }
            )
        }


class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }


class NewComboForm(forms.ModelForm):
    class Meta:
        model = Combo
        fields = '__all__'
        exclude = ('product_list',)

        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'price': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }


class NewComboDetailForm(forms.ModelForm):
    class Meta:
        model = ComboDetail
        fields = '__all__'


        widgets = {
            'product': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ), 
            'quantity': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }


ComboDetailInlineFormSet = forms.inlineformset_factory(
    Combo, 
    ComboDetail, 
    form=NewComboDetailForm, 
    extra=4,
    max_num=4
)