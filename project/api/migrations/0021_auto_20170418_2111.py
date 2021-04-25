# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_auto_20170418_1652"),
    ]

    operations = [
        migrations.AlterField(
            model_name="civi",
            name="c_type",
            field=models.CharField(
                default=b"problem",
                max_length=31,
                choices=[
                    (b"problem", b"Problem"),
                    (b"cause", b"Cause"),
                    (b"solution", b"Solution"),
                    (b"response", b"Response"),
                    (b"rebuttal", b"Rebuttal"),
                ],
            ),
        ),
    ]
