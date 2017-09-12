# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(max_length=255, choices=[(b'vote_vneg', b'Vote Strongly Disagree'), (b'vote_neg', b'Vote Disagree'), (b'vote_neutral', b'Vote Neutral'), (b'vote_pos', b'Vote Agree'), (b'vote_vpos', b'Vote Strongly Agree'), (b'favorite', b'Favorite')]),
        ),
    ]
