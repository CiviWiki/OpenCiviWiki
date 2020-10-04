# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20161215_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('district', models.CharField(max_length=63)),
                ('state', models.CharField(max_length=63)),
                ('level', models.CharField(default=b'federal', max_length=31, choices=[(b'federal', b'Federal'), (b'state', b'State')])),
                ('term_start', models.DateField()),
                ('term_end', models.DateField()),
                ('party', models.CharField(max_length=127)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),
            ],
        ),
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
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=1023)),
                ('short_title', models.CharField(max_length=1023)),
                ('short_summary', models.CharField(max_length=1023)),
                ('number', models.IntegerField(default=0)),
                ('b_type', models.CharField(max_length=63)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='civi',
            name='bill',
            field=models.ForeignKey(default=None, to='api.Bill', null=True, on_delete=models.PROTECT),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(default=b'abstain', max_length=31, choices=[(b'yes', b'Yes'), (b'no', b'No'), (b'abstain', b'Abstain')])),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('bill', models.ForeignKey(default=None, to='api.Bill', null=True, on_delete=models.PROTECT)),
                ('representative', models.ForeignKey(default=None, to='api.Representative', null=True, on_delete=models.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Rationale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('body', models.TextField(max_length=4095)),
                ('votes_vneg', models.IntegerField(default=0)),
                ('votes_neg', models.IntegerField(default=0)),
                ('votes_neutral', models.IntegerField(default=0)),
                ('votes_pos', models.IntegerField(default=0)),
                ('votes_vpos', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('bill', models.ForeignKey(default=None, to='api.Bill', null=True, on_delete=models.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='rationale',
            name='vote',
            field=models.ForeignKey(default=None, to='api.Vote', null=True, on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='rationale',
            name='representative',
            field=models.ForeignKey(default=None, to='api.Representative', null=True, on_delete=models.PROTECT),
        ),

    ]
