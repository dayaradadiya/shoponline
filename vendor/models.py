from datetime import datetime
from django.utils import timezone
from django.db import models

from accounts.models import User,UserProfile
from accounts.utils import send_notification
from accounts.validators import validate_file_mimetype
from django.core.validators import FileExtensionValidator

ext_validator = FileExtensionValidator(['jpg','png','jpeg']) 

class Vendor(models.Model):
    INDIVISUAL = 1
    BUSINESS = 2
    SELLER_CHOICE = (
        (INDIVISUAL,'Indivisual'),
        (BUSINESS,'Business')
    )
    user = models.OneToOneField(User, related_name="user",on_delete = models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name="userprofile",on_delete = models.CASCADE)
    vendor_name = models.CharField(max_length=100, blank=True,null=True)
    vendor_slug = models.SlugField(max_length=100, unique=True,null=True)
    vendor_liscence = models.FileField(upload_to='vendor/liscence',blank=True,null=True,validators=[ext_validator,validate_file_mimetype])
    free_del_amount_limit = models.IntegerField(default=9999, null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)
    stype = models.PositiveSmallIntegerField(choices=SELLER_CHOICE,blank=True,null=True)
    

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                        'user' : self.user,
                        'is_approved' : self.is_approved,
                        'to_email' : self.user.email
                    }
                if self.is_approved == True:
                    mail_subject = "Congratulations! your shop has been approved."
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject = "We're sorry! You are not eligible for publishing your product menu on our marketplace."
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor, self).save(*args,**kwargs)

