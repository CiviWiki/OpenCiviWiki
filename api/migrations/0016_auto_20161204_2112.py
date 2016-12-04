# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import api.models.account


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20161103_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='category',
        ),
        migrations.RemoveField(
            model_name='account',
            name='issues',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='children',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='parents',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='topic',
        ),
        migrations.AddField(
            model_name='civi',
            name='links',
            field=models.ManyToManyField(related_name='_links_+', to='api.Civi'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(default=b'profile/happy.png', null=True, upload_to=api.models.account.PathAndRename(b'profile/'), blank=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=127),
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
