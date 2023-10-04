from django import forms
from accounts import validators
from accounts.validators import allow_only_images_validator
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from  .models import Bank, Bank_Account_Info, ICProfile, User, UserProfile
from django.forms import DateField, DateInput, ValidationError
from django.contrib.auth import password_validation


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())



    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class' : 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password',
        'class' : 'form-control',
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class' : 'form-control',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Username',
        'class' : 'form-control',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Last Name',
        'class' : 'form-control',
    })) 

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Enter Email Address',
        'class' : 'form-control',
    }))

    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Phone Number',
        'class' : 'form-control',
    }))

 
class AddUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())



    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password','role']

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class' : 'form-control',
    }))


    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class' : 'form-control',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Username',
        'class' : 'form-control',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Last Name',
        'class' : 'form-control',
    })) 

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Enter Email Address',
        'class' : 'form-control',
    }))

    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Phone Number',
        'class' : 'form-control',
    }))

    ROLE_CHOICES = [
    (1, "VENDOR"),
    (2, "CUSTOMER")]    
        
    role = forms.CharField(
        widget=forms.Select(choices=ROLE_CHOICES,attrs={
             'class' : 'form-control', 
        })
    )


class EditUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())



    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class' : 'form-control',
    }))


    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class' : 'form-control',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Username',
        'class' : 'form-control',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Last Name',
        'class' : 'form-control',
    })) 

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Enter Email Address',
        'class' : 'form-control',
    }))

    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Phone Number',
        'class' : 'form-control',
    }))





    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("password does not match!")
class DateInput(DateInput):
         input_type = 'date'
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields=['profile_picture','address','country','pin_code','unit_no','alt_phone_number']
        # widgets = {
        #     'profile_picture' : forms.FileInput(attrs={'accept':'.jpg,.png,.jpeg'})
        # }



    profile_picture = forms.FileField(widget=forms.FileInput(attrs={
        'accept':'.jpg,.png,.jpeg',
        'class' : 'btn btn-info', })
       )
    address = forms.CharField(widget=forms.TextInput(attrs=
        {'required':'required',
        'class' : 'form-control',
    }))

    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Country',
        'class' : 'form-control',
    }))

    unit_no = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Unit No',
        'class' : 'form-control',
    }))

    alt_phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter phone no',
        'class' : 'form-control',
    }))


    pin_code = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Postal Code',
        'class' : 'form-control',
    }))

    

    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model =User
        fields = ['first_name','last_name','phone_number']

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class' : 'form-control',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Last Name',
        'class' : 'form-control',
    }))

    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Enter Phone number',
        'class' : 'form-control',
    }))

class ICProfileForm(forms.ModelForm):
    class Meta:
        model = ICProfile
        fields=['full_name_ic','ic_type','fin_no','fin_expiry_date','ic_photo','date_of_birth','nationality']


    IC_CHOICES = [
        (1, "FIN"),
        (2, "NRIC")]    
            
    full_name_ic = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Full Name as per NRIC/FIN',
        'class' : 'form-control',
    }))

    ic_type = forms.IntegerField(
        widget=forms.Select(choices=IC_CHOICES,attrs={
             'class' : 'form-control', 
        })
    )

    fin_no = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter FIN/NRIC',
        'class' : 'form-control',
    }))

    fin_expiry_date = DateField(widget=DateInput)

    

    ic_photo = forms.FileField(widget=forms.FileInput(attrs={
        'accept':'.jpg,.png,.jpeg',
        'class' : 'btn btn-info', }),
       )

    
    # BIRTH_YEAR_CHOICES = [year for year in range(1918, 2023)]
    # date_of_birth = forms.DateField(
    #     widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES,
    #                                    attrs={"class": "form-control"}
    # ))

    date_of_birth = DateField(widget=DateInput)

    nationality = CountryField().formfield(
        widget=CountrySelectWidget(
           attrs={"class": "form-control"}
        )
    )

class BankAccForm(forms.ModelForm):
    class Meta:
        model = Bank_Account_Info
        fields=['bank_doc','bank_acc_holder_name','acc_no','bank_name','branch_name']

    bank_doc = forms.FileField(widget=forms.FileInput(attrs={
        'accept':'.jpg,.png,.jpeg',
        'class' : 'btn btn-info', }),
       )

    bank_acc_holder_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Bank account holder name',
        'class' : 'form-control',
    }))

    acc_no = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Acc No',
        'class' : 'form-control',
    }))

    bank_name =  forms.ModelChoiceField(
         queryset = Bank.objects.all(),
         initial = Bank.objects.all().first
    )

    

    branch_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Branch',
        'class' : 'form-control',
    }))
