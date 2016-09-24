# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20160908_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='account',
            name='representatives',
            field=models.ManyToManyField(related_name='_representatives_+', to='api.Account'),
        ),
    ]
