# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20160922_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='issues',
            field=models.ManyToManyField(related_name='issues', to='api.Thread'),
        ),
    ]
