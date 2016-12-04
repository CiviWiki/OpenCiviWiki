# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20161009_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='category',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
