from django.db import models

# Create your models here.


class Mappings(models.Model):
    name = models.CharField(max_length=100, null=True)
    value = models.FloatField(default=0, blank=True, null=True)
