# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170110_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='civi',
            name='linked_civis',
            field=models.ManyToManyField(related_name='_linked_civis_+', to='api.Civi'),
        ),
    ]
