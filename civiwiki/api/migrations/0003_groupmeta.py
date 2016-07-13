# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('api', '0002_account_beta_access'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=63)),
                ('description', models.TextField(max_length=4095)),
                ('profile_image', models.CharField(max_length=255)),
                ('cover_image', models.CharField(max_length=255)),
                ('group', models.ForeignKey(related_name='group', to='auth.Group')),
            ],
        ),
    ]
