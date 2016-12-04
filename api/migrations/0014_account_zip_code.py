# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_account_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='zip_code',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
