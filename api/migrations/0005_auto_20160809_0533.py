# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160715_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=63)),
                ('body', models.TextField(max_length=4095)),
                ('sources', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('votes_negative2', models.IntegerField(default=0)),
                ('votes_negative1', models.IntegerField(default=0)),
                ('votes_neutral', models.IntegerField(default=0)),
                ('votes_positive1', models.IntegerField(default=0)),
                ('votes_positive2', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(default=None, to='api.Account', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=63)),
                ('summary', models.CharField(max_length=4095)),
                ('facts', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=1023, blank=True), blank=True)),
                ('category', models.ForeignKey(default=None, to='api.Category', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='civi',
            name='and_negative',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='and_positive',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='at',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='category',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='type',
        ),
        migrations.AddField(
            model_name='civi',
            name='bill_against',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='bill_for',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='bill_source',
            field=models.CharField(default=None, max_length=127, null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='sources',
            field=django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='cause',
            field=models.ManyToManyField(related_name='cause', to='api.Civi'),
        ),
        migrations.AddField(
            model_name='thread',
            name='contributors',
            field=models.ManyToManyField(to='api.Account'),
        ),
        migrations.AddField(
            model_name='thread',
            name='problem',
            field=models.ManyToManyField(related_name='problem', to='api.Civi'),
        ),
        migrations.AddField(
            model_name='thread',
            name='solution',
            field=models.ManyToManyField(related_name='solution', to='api.Civi'),
        ),
        migrations.AddField(
            model_name='thread',
            name='topic',
            field=models.ForeignKey(default=None, to='api.Topic', null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='response',
            field=models.ManyToManyField(to='api.Response'),
        ),
        migrations.AddField(
            model_name='civi',
            name='thread',
            field=models.ForeignKey(default=None, to='api.Thread', null=True),
        ),
    ]
