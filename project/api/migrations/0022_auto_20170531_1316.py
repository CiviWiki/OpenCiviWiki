# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_auto_20170418_2111"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
