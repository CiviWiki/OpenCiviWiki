# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20160921_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='issues',
            field=models.ManyToManyField(related_name='issues', to='api.Hashtag'),
        ),
        migrations.AlterField(
            model_name='account',
            name='representatives',
            field=models.ManyToManyField(related_name='representatives', to='api.Representative'),
        ),
    ]
