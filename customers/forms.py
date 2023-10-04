from django import forms
from customers.models import Address
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from orders.models import  Refund, Return_main_reason, Return_reason
from dynamic_forms import DynamicField, DynamicFormMixin

# class OrderProductForm(forms.ModelForm):
#        class Meta:
#         model = OrderProduct
#         fields = ['message','reason','email','ref_code','order','payment','user','product','variations','variant','quantity','product_price']

class RefundForm(DynamicFormMixin, forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['additional_information','main_reason','reason']

    def reason_choices(form):
         main_reason = form['main_reason'].value()
         return Return_reason.objects.filter(main_reason=main_reason)

    additional_information = forms.CharField(widget=forms.Textarea(attrs={
                     'class' : 'form-control',
              }))
       
    

    main_reason = forms.ModelChoiceField(
         queryset = Return_main_reason.objects.all(),
         initial = Return_main_reason.objects.all().first
    )
    
    reason = DynamicField(
         forms.ModelChoiceField,
         queryset = reason_choices,
        #  initial = initial_module,
    )
            
        
    # pickup_date = forms.DateField(widget=forms.DateInput)

    #  pickup_date =  forms.DateTimeField(
    #     widget=DateTimePicker(options={
    #         "format": "YYYY-MM-DD",
    #         "pickTime": False}
    #     ))

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields =[ 'first_name','last_name' ,'mobile' ,'address_line_1' , 'unit_no'  ,'country' , 'postal_code']

        country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Country',
        'class' : 'form-control',
    }))

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['return_pickup_date',]

    # pickup_date = forms.DateField(widget=forms.DateInput)
    return_pickup_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))