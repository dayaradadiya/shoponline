# Generated by Django 3.2.18 on 2023-09-28 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20230926_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='free_del_amount_limit',
        ),
    ]
