# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-02 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_institutional_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='institutional_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
