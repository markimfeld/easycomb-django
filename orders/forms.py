from django import forms

# --------------
from .models import Order, OrderDetail

class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('status','paid_status', 'money_received', 'combos', 'products')
        widgets = {
            'customer': forms.Select(
                attrs = {
                    'class': 'form-control select2bs4'
                }
            )
        }

class NewOrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        exclude = ('price_combo', 'price_product')
        widgets = {
            'combo': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            ),
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
            'quantity': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            )   
        }

OrderDetailInlineFormSet = forms.inlineformset_factory(
    Order,
    OrderDetail,
    form=NewOrderDetailForm,
    extra=4
)