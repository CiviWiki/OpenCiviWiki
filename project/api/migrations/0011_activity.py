# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20170110_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(max_length=255, choices=[(b'vote_vneg', b'Vote Strongly Disagree'), (b'vote_veg', b'Vote Disagree'), (b'vote_neutral', b'Vote Neutral'), (b'vote_pos', b'Vote Agree'), (b'vote_vpos', b'Vote Strongly Agree'), (b'favorite', b'Favorite')])),
                ('read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),
                ('civi', models.ForeignKey(default=None, to='api.Civi', null=True, on_delete=models.PROTECT)),
                ('thread', models.ForeignKey(default=None, to='api.Thread', null=True, on_delete=models.PROTECT)),
            ],
        ),
    ]
