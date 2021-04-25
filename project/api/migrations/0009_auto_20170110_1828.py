# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import api.models.account


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_auto_20170110_0850"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="profile_image",
            field=models.ImageField(
                null=True,
                upload_to=api.models.account.PathAndRename(b"profile/"),
                blank=True,
            ),
        ),
    ]
