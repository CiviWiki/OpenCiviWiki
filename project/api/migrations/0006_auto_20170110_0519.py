# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170109_1813'),
    ]

    operations = [

        migrations.RemoveField(
            model_name='civi',
            name='related_civis',
        ),
        # migrations.AddField(
        #     model_name='civi',
        #     name='links',
        #     field=models.ManyToManyField(related_name='_civi_links_+', to='api.Civi'),
        # ),
        # migrations.RemoveField(
        #     model_name='civi',
        #     name='links',
        # ),

        migrations.AddField(
            model_name='civi',
            name='linked_civis',
            field=models.ManyToManyField(related_name='_linked_civis_+', to='api.Civi'),
        ),
        migrations.AddField(
            model_name='civi',
            name='response_civis',
            field=models.ForeignKey(related_name='responses', to='api.Civi', null=True, on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name='civi',
            name='body',
            field=models.CharField(max_length=1023),
        ),
    ]
