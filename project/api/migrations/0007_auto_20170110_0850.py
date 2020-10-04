# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20170110_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='civi',
            name='votes_neg',
            field=models.IntegerField(default=0),
        ),

        migrations.AddField(
            model_name='civi',
            name='votes_pos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='civi',
            name='votes_vneg',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='civi',
            name='votes_vpos',
            field=models.IntegerField(default=0),
        ),

        migrations.RenameField(
            model_name='civi',
            old_name='votes_neg',
            new_name='vote_neg',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_neutral',
            new_name='vote_neutral',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_pos',
            new_name='vote_pos',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_vneg',
            new_name='vote_vneg',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_vpos',
            new_name='vote_vpos',
        ),
        migrations.AlterField(
            model_name='civi',
            name='linked_civis',
            field=models.ManyToManyField(default=None, related_name='_linked_civis_+', null=True, to='api.Civi'),
        ),
        migrations.AlterField(
            model_name='civi',
            name='response_civis',
            field=models.ForeignKey(related_name='responses', default=None, to='api.Civi', null=True, on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name='civi',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
