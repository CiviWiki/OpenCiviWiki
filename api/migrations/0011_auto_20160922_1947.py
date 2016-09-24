# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import api.models.account


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_account_representatives'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(null=True, upload_to=api.models.account.get_profile_path, blank=True),
        ),
    ]
