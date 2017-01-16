# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20161227_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='categories',
            field=models.ManyToManyField(related_name='user_categories', to='api.Category'),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_civis',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_solutions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_views',
            field=models.IntegerField(default=0),
        ),
    ]
