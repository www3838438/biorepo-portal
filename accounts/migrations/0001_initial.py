# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.management import call_command
from django.db import migrations, models
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
import django.db.models.deletion

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
fixture_filename = '0001_eula.json'

def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)
    call_command('loaddata', fixture_file)

def unload_fixture(apps, schema_editor):
    FlatPage.objects.all().delete()
    Site.objects.all().delete()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=100, null=True)),
                ('eula', models.BooleanField(default=False)),
                ('reason', models.TextField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(load_fixture, reverse_code=unload_fixture)
    ]
