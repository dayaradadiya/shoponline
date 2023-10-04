
from django import forms


from  .models import CartItem


class ShopCartForm(forms.ModelForm):


    class Meta:
        model = CartItem
        fields = ['quantity']

    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
    }))

 