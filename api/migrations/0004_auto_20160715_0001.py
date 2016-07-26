# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_groupmeta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='admins',
        ),
        migrations.RemoveField(
            model_name='group',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='group',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='groupmeta',
            name='group',
        ),
        migrations.RemoveField(
            model_name='account',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='group',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='GroupMeta',
        ),
    ]
