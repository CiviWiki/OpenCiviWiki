# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20161215_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='bioguideID',
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='representative',
            name='senate_class',
            field=models.CharField(max_length=63, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='representative',
            name='district',
            field=models.CharField(max_length=63, null=True, blank=True),
        ),
    ]
