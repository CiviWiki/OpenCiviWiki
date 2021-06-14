# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_auto_20170331_1233"),
    ]

    operations = [
        migrations.AddField(
            model_name="representative",
            name="official_full_name",
            field=models.CharField(max_length=127, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="account",
            name="representatives",
            field=models.ManyToManyField(
                related_name="account", to="api.Representative"
            ),
        ),
    ]
