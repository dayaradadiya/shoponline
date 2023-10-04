from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name