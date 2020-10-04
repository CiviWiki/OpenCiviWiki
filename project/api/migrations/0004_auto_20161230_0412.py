# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20161227_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=511)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('summary', models.CharField(max_length=4095)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),
                ('category', models.ForeignKey(default=None, to='api.Category', null=True, on_delete=models.PROTECT)),
                ('facts', models.ManyToManyField(to='api.Fact')),
                ('hashtags', models.ManyToManyField(to='api.Hashtag')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(default=b'new_follower', max_length=31, choices=[(b'new_follower', b'New follower'), (b'response_to_yout_civi', b'Response to your civi'), (b'rebuttal_to_your_response', b'Rebuttal to your response')])),
                ('read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),
                ('civi', models.ForeignKey(default=None, to='api.Civi', null=True, on_delete=models.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='thread',
            field=models.ForeignKey(default=None, to='api.Thread', null=True, on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='civi',
            name='thread',
            field=models.ForeignKey(default=None, to='api.Thread', null=True, on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='account',
            name='categories',
            field=models.ManyToManyField(related_name='user_categories', to='api.Category'),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_civis',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_solutions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_views',
            field=models.IntegerField(default=0),
        ),
    ]
