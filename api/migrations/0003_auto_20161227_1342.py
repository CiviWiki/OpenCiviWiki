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
                ('account', models.ForeignKey(default=None, to='api.Account', null=True)),
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
    ]
