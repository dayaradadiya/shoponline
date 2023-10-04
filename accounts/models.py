from datetime import datetime
from django.utils import timezone
from django.db import models
from asgiref.sync import async_to_sync,sync_to_async
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator
import magic
from django.core.exceptions import ValidationError
import uuid
from accounts.validators import validate_file_mimetype

# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("user must have an email address")
        if not username:
            raise ValueError("user must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name,last_name,username,email,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



# class User(AbstractBaseUser,PermissionsMixin):
class User(AbstractBaseUser,PermissionsMixin):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=12,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    # required fields
    date_joined = models.DateTimeField(default=datetime.now)
    last_login = models.DateTimeField(default=datetime.now)
    created_date = models.DateTimeField(default=datetime.now)
    modified_date = models.DateTimeField(default=datetime.now)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = UserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email
    def has_perm(self,perm, obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def get_role(self):
        if self.role==1:
            user_role = 'Vendor'
        elif self.role==2:
            user_role = 'Customer'
        return user_role
    @staticmethod 
    def given_user_details(id):
        print('given_user_details id is ',id)
        instance =  User.objects.get(id=id)
        data = {}
        data['email'] = instance.email
        data['first_name'] = instance.first_name
        return data

ext_validator = FileExtensionValidator(['jpg','png','jpeg'])       

class UserProfile(models.Model):
    FIN = 1
    NRIC = 2

    IC_CHOICE = (
        (FIN,'FIN'),
        (NRIC,'NRIC')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.FileField(upload_to='users/profile_pictures',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    full_name_ic = models.CharField(max_length=250, blank=True, null=True)
    ic_type = models.PositiveSmallIntegerField(choices=IC_CHOICE,blank=True,null=True)
    fin_no = models.CharField(max_length=9, blank=True, null=True)
    fin_expiry_date = models.CharField(max_length=6, blank=True, null=True)
    ic_photo = models.FileField(upload_to='users/ic_photos',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
    date_of_birth = models.DateField( blank=True, null=True)
    nationality =  CountryField(blank_label="(select country)")
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)
    unit_no = models.CharField(max_length=15, blank=True, null=True)
    alt_phone_number = models.CharField(max_length=12,blank=True, null=True)

    def __str__(self):
        return self.user.email
    
class BusinessProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
        company_name = models.CharField(max_length=100, null=True,blank=True)
        license_number = models.CharField(max_length=10, null=True,blank=True)
        entity_type = models.CharField(max_length=100, null=True,blank=True)
        company_address = models.CharField(max_length=250, null=True,blank=True)
        license_document = models.FileField(upload_to='users/liscence_document',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])

        def __str__(self):
         return self.user.email
    
class ICProfile(models.Model):
    FIN = 1
    NRIC = 2

    IC_CHOICE = (
        (FIN,'FIN'),
        (NRIC,'NRIC')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True)
    full_name_ic = models.CharField(max_length=250, blank=True, null=True)
    ic_type = models.PositiveSmallIntegerField(choices=IC_CHOICE,blank=True,null=True)
    fin_no = models.CharField(max_length=9, blank=True, null=True)
    fin_expiry_date = models.DateField(blank=True, null=True)
    ic_photo = models.FileField(upload_to='users/ic_photos',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
    date_of_birth = models.DateField( blank=True, null=True)
    nationality =  CountryField(blank_label="(select country)")
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
         return self.user.email
class Bank(models.Model):
    bank_name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
         return self.bank_name
    
class Bank_Account_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True)
    bank_doc = models.FileField(upload_to='users/account_info',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
    bank_acc_holder_name = models.CharField(max_length=250, blank=True, null=True)
    acc_no = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.ForeignKey(Bank,on_delete=models.CASCADE,blank=True, null=True)
    branch_name = models.CharField(max_length=250, blank=True, null=True)

    # def __str__(self):
    #      return self.user