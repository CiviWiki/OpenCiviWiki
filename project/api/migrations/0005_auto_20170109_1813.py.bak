# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20161230_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='civi',
            name='related_civis',
            field=models.ManyToManyField(related_name='_related_civis_+', to='api.Civi'),
        ),
        migrations.AlterField(
            model_name='civi',
            name='c_type',
            field=models.CharField(default=b'problem', max_length=31, choices=[(b'problem', b'Problem'), (b'cause', b'Cause'), (b'solution', b'Solution'), (b'response', b'Response')]),
        ),
        migrations.AddField(
            model_name='civi',
            name='links',
            field=models.ManyToManyField(related_name='link', to='api.Civi'),
        ),
    ]
