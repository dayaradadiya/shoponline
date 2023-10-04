import datetime
from typing import Any, Optional
from django.core.management.base import BaseCommand

from datetime import timedelta, date

from accounts.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs) :
           users =  User.objects.filter(is_active=False)
           today = date.today()
           for x in users:
                start_date = x.date_joined.date()
                end_date = start_date + timedelta(days=3)

                if end_date < today:
                     User.objects.get(pk=x.id).delete()
                     print(f'just deleted {x.username}')
