"""shoponline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
# from customadmin.admin import customadmin_site
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.admin import OTPAdminSite

class OTPAdmin(OTPAdminSite):
    pass
# admin_site = OTPAdmin(name="OTPAdmin")
admin.site.__class__ = OTPAdminSite
# admin.site.register(TOTPDevice)

urlpatterns = [
    # path('dj-admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    
    path('loginsecure/', admin.site.urls),
    # path('customadmin/', customadmin_site.urls),
    path('admin/', include('customadmin.urls')),
    path('',views.home, name='home'),
    path('',include('accounts.urls')),
    path('store/',include('store.urls')),
    path('cart/',include('cart.urls')),
    path('marketplace/',include('marketplace.urls')),
    path('orders/',include('orders.urls')),

    path('djrichtextfield/', include('djrichtextfield.urls')),

    path('', include('chat.urls')),
    path('', include('django_dyn_dt.urls')),

    path('shipping/',include('shipping.urls')),
    
    path('mass_upload/',include('mass_upload.urls')),

]


urlpatterns = urlpatterns + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

