from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from orders.models import Order
 
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'unit_no',  'country',  'order_note','pin_code']

        

        first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class' : 'form-control',
    }))


        last_name = forms.CharField(widget=forms.TextInput(attrs={
            'class' : 'form-control',
        }))

        country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Country',
        'class' : 'form-control',
    }))

        address_line_1 = forms.CharField(widget=forms.TextInput(attrs={
            'class' : 'form-control',
        }))

        order_note = forms.CharField(widget=forms.TextInput(attrs={
            'class' : 'form-control',
        })) 

        email = forms.CharField(widget=forms.EmailInput(attrs={
            'class' : 'form-control',
             'type': 'email',
             'id' : 'checkout-email',
        }))

        phone = forms.CharField(widget=forms.NumberInput(attrs={
            'class' : 'form-control',
        }))
        pin_code = forms.CharField(widget=forms.NumberInput(attrs={
            'class' : 'form-control',
        }))


        

    # def clean(self):
    #     cleaned_data = super(OrderForm,self).clean() 

