# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20161018_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='followers',
            field=models.ManyToManyField(related_name='_followers_+', to='api.Account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='_following_+', to='api.Account'),
        ),
    ]
