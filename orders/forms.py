from django import forms
from django.utils.translation import gettext_lazy as _

# --------------
from clients.models import Customer
from inventory.models import Combo
from .models import Order, OrderDetail, Income, Status


class ChangeStatusOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {
            'status': forms.Select(
                attrs = {
                    'class': 'form-control custom-select'
                }
            )
        }

class NewIncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        exclude = ('order',)
        widgets = {
            'date': forms.DateInput(
                attrs = {
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#reservationdate'
                }
            ),
            'amount': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }


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
    
    def __init__(self, *args, **kwargs):
        super(NewOrderForm, self).__init__(*args, **kwargs)
        customers = Customer.objects.filter(status=True)
        options = [(customer.id, customer.first_name) for customer in customers]
        self.fields['customer'].choices = options 

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
            'description': forms.TextInput(
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
    
    def __init__(self, *args, **kwargs):
        super(NewOrderDetailForm, self).__init__(*args, **kwargs)
        self.fields['combo'].queryset = Combo.objects.filter(status=True)

OrderDetailInlineFormSet = forms.inlineformset_factory(
    Order,
    OrderDetail,
    form=NewOrderDetailForm,
    extra=1
)
