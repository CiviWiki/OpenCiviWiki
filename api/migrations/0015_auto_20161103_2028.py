# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_account_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='full_account',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(default=b'/media/profile/happy.png', null=True, upload_to=b'profile/', blank=True),
        ),
    ]
