from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import pyotp


from datetime import datetime,timedelta
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
def send_verification_email(request,user,mail_subject,email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,
    {
        'user':user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    }
    )
    to_email = user.email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()


def send_verification_email(request,user,mail_subject,email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,
    {
        'user':user,
        'domain' : current_site,
        'uid' :urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    }
    )
    to_email = user.email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.content_subtype = "html"
    mail.send()

def send_notification(mail_subject,mail_template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    if(isinstance(context['to_email'] ,str)):
        to_email = []
        to_email.append(context['to_email'] )
    else:
        to_email = context['to_email'] 
    mail = EmailMessage(mail_subject,message,from_email,to=to_email)
    mail.content_subtype = "html"
    mail.send()

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(),interval=60)
    otp=totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)  
    request.session['otp_valid_date'] = str(valid_date)

    print(f'otp is : {otp}')

    mail_subject = "Your account needs to be verified"
    email_template = 'accounts/emails/account_login.html'
    user = request.user

    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,
    {
        'user':user,
        'domain' : current_site,
        'otp': str(otp),
    }
    )
    
    to_email = request.session['email']
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.content_subtype = "html"
    mail.send()


# from django_otp import devices_for_user
# from django_otp.plugins.otp_totp.models import TOTPDevice
# def get_user_totp_device(user, confirmed=None):
#     devices = devices_for_user(user, confirmed=confirmed)
#     for device in devices:
#         if isinstance(device, TOTPDevice):
#             return device


# def send_otp(request):
#     user = request.user
#     device = get_user_totp_device(user)
#     if not device:
#             device = user.totpdevice.create(confirmed=False)
#     url = device.config_url
#     print('url is :',url)
