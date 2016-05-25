# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='immutable_key',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.ImmutableKey'),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='immutable_key',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.ImmutableKey'),
        ),
    ]