# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=63)),
                ('last_name', models.CharField(max_length=63)),
                ('email', models.CharField(unique=True, max_length=63)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('about_me', models.CharField(max_length=511, blank=True)),
                ('valid', models.BooleanField(default=False)),
                ('profile_image', models.CharField(max_length=255)),
                ('cover_image', models.CharField(max_length=255)),
                ('statistics', models.TextField(blank=True)),
                ('interests', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('civi_pins', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('civi_history', django.contrib.postgres.fields.ArrayField(default=[], size=10, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('friend_requests', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('award_list', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('zip_code', models.CharField(max_length=6, blank=True)),
                ('country', models.CharField(max_length=46, blank=True)),
                ('state', models.CharField(max_length=63, blank=True)),
                ('city', models.CharField(max_length=63, blank=True)),
                ('address1', models.CharField(max_length=255, blank=True)),
                ('address2', models.CharField(max_length=255, blank=True)),
                ('friends', models.ManyToManyField(related_name='friended_account', to='api.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Civi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=63)),
                ('body', models.TextField(max_length=4095)),
                ('votes_negative2', models.IntegerField(default=0)),
                ('votes_negative1', models.IntegerField(default=0)),
                ('votes_neutral', models.IntegerField(default=0)),
                ('votes_positive1', models.IntegerField(default=0)),
                ('votes_positive2', models.IntegerField(default=0)),
                ('visits', models.IntegerField(default=0)),
                ('type', models.CharField(default='I', max_length=2)),
                ('reference', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('at', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('and_negative', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('and_positive', django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=127, blank=True), blank=True)),
                ('category', models.ForeignKey(default=None, to='api.Category', null=True)),
                ('creator', models.ForeignKey(default=None, to='api.Account', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=511)),
                ('author', models.ForeignKey(to='api.Account')),
                ('civi', models.ForeignKey(to='api.Civi')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=63)),
                ('description', models.TextField(max_length=4095)),
                ('profile_image', models.CharField(max_length=255)),
                ('cover_image', models.CharField(max_length=255)),
                ('admins', models.ManyToManyField(related_name='group_admin', to='api.Account')),
                ('contributors', models.ManyToManyField(related_name='group_member', to='api.Account')),
                ('owner', models.ForeignKey(related_name='group_owner', to='api.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='', max_length=63)),
                ('votes_negative2', models.IntegerField(default=0, null=True)),
                ('votes_negative1', models.IntegerField(default=0, null=True)),
                ('votes_neutral', models.IntegerField(default=0, null=True)),
                ('votes_positive1', models.IntegerField(default=0, null=True)),
                ('votes_positive2', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=63)),
                ('bill', models.URLField(null=True)),
                ('category', models.ForeignKey(to='api.Category')),
            ],
        ),
        migrations.AddField(
            model_name='civi',
            name='group',
            field=models.ForeignKey(default=None, to='api.Group', null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='hashtags',
            field=models.ManyToManyField(to='api.Hashtag'),
        ),
        migrations.AddField(
            model_name='civi',
            name='topic',
            field=models.ForeignKey(default=None, to='api.Topic', null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='civi',
            field=models.ForeignKey(to='api.Civi'),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(related_name='user_groups', to='api.Group'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
