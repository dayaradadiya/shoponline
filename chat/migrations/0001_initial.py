# Generated by Django 3.2.18 on 2023-09-24 06:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('sent_by', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='UserContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ManyToManyField(blank=True, related_name='_chat_usercontacts_friends_+', to='chat.UserContacts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=300)),
                ('client', models.CharField(max_length=255)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('active', 'Active'), ('closed', 'Closed')], default='waiting', max_length=20)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to=settings.AUTH_USER_MODEL)),
                ('messages', models.ManyToManyField(blank=True, to='chat.Message')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
