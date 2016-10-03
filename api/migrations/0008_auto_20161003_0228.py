# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_civi_children'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='civi',
            name='parents',
        ),
        migrations.AddField(
            model_name='civi',
            name='links',
            field=models.ManyToManyField(related_name='_civi_links_+', to='api.Civi'),
        ),
    ]
