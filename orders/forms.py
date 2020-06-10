from django import forms

# --------------
from .models import Order, OrderDetail

class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('status','paid_status', 'money_received', 'total', 'combos', 'products')
        widgets = {
            'customer': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            )
        }

class NewOrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        exclude = ('price_unit',)
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