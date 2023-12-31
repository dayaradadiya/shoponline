# Generated by Django 3.2.18 on 2023-09-26 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20230926_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='parcel_size_H',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='parcel_size_L',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='parcel_size_W',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
