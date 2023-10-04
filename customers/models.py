from django.db import models
from django.core.validators import MaxValueValidator
from accounts.models import User

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=8, blank=True, null=True)
    address_line_1 = models.CharField(max_length=100, null=True)
    unit_no  = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    country = models.CharField(max_length=15, null=True,blank=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.email
    
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
    
    class Meta:
        verbose_name_plural = "Address"

