# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_civi_links'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='civi',
            name='bill',
        ),
        migrations.AddField(
            model_name='civi',
            name='bill',
            field=models.ManyToManyField(to='api.Bill'),
        ),
    ]
