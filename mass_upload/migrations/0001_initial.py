# Generated by Django 3.2.18 on 2023-09-24 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock_keeping_unit',
            fields=[
                ('sku', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variants')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='StgProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('product_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('featured_image', models.CharField(blank=True, max_length=1000, null=True)),
                ('image1', models.CharField(blank=True, max_length=1000, null=True)),
                ('image2', models.CharField(blank=True, max_length=1000, null=True)),
                ('image3', models.CharField(blank=True, max_length=1000, null=True)),
                ('image4', models.CharField(blank=True, max_length=1000, null=True)),
                ('image5', models.CharField(blank=True, max_length=1000, null=True)),
                ('image6', models.CharField(blank=True, max_length=1000, null=True)),
                ('image7', models.CharField(blank=True, max_length=1000, null=True)),
                ('image8', models.CharField(blank=True, max_length=1000, null=True)),
                ('brand', models.CharField(blank=True, max_length=1000, null=True)),
                ('product_information', models.TextField(blank=True, null=True)),
                ('variant', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_title', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_color', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_size', models.CharField(blank=True, max_length=1000, null=True)),
                ('image_variant', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_stock', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_price', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_discount', models.CharField(blank=True, max_length=1000, null=True)),
                ('variant_max_allowed_quantity', models.CharField(blank=True, max_length=1000, null=True)),
                ('stock', models.CharField(blank=True, max_length=1000, null=True)),
                ('price', models.CharField(blank=True, max_length=1000, null=True)),
                ('discount', models.CharField(blank=True, max_length=1000, null=True)),
                ('weight', models.CharField(blank=True, max_length=1000, null=True)),
                ('parcel_size_L', models.CharField(blank=True, max_length=1000, null=True)),
                ('parcel_size_W', models.CharField(blank=True, max_length=1000, null=True)),
                ('parcel_size_H', models.CharField(blank=True, max_length=1000, null=True)),
                ('max_allowed_quantity', models.CharField(blank=True, max_length=1000, null=True)),
                ('min_order_quantity', models.CharField(blank=True, max_length=1000, null=True)),
                ('free_del_amount_limit', models.CharField(blank=True, max_length=1000, null=True)),
                ('file_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, max_length=1000, null=True)),
                ('error', models.CharField(blank=True, max_length=1000, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(blank=True, max_length=100, null=True)),
                ('processed', models.IntegerField(blank=True, default=0, null=True)),
                ('products', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.CharField(choices=[('Successful', 'Successful'), ('Unsuccessful', 'Unsuccessful'), ('Partially Successful', 'Partially Successful'), ('Upload Failed', 'Upload Failed')], max_length=100)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
        ),
    ]