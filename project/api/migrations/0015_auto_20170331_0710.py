# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import api.models.civi
import api.models.account


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20170124_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='CiviImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=api.models.civi.PathAndRename(b'/'), blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('civi', models.ForeignKey(related_name='images', to='api.Civi', on_delete=models.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='representative',
            name='about_me',
            field=models.CharField(max_length=511, blank=True),
        ),
        migrations.AddField(
            model_name='representative',
            name='first_name',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='representative',
            name='last_name',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(null=True, upload_to=api.models.account.PathAndRename(b'/'), blank=True),
        ),
    ]
