# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0022_auto_20170531_1316"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="profile_image_thumb",
            field=models.ImageField(
                null=True, upload_to=accounts.models.PathAndRename(b""), blank=True
            ),
        ),
    ]
