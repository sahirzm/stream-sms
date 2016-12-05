# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 17:53
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import ss_utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255, validators=[ss_utils.validators.NameValidator('first_name'), django.core.validators.MinLengthValidator(2)])),
                ('middle_name', models.CharField(blank=True, max_length=255, validators=[ss_utils.validators.NameValidator('middle_name')])),
                ('last_name', models.CharField(max_length=255, validators=[ss_utils.validators.NameValidator('last_name'), django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('mobile', models.CharField(max_length=15, unique=True, validators=[ss_utils.validators.PhoneValidator('mobile', 'Invalid mobile number')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
        ),
    ]
