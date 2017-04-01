# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20170331_0710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='civiimage',
            name='last_modified',
        ),
    ]
