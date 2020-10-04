# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import api.models.account


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
                ('about_me', models.CharField(max_length=511, blank=True)),
                ('longitude', models.DecimalField(default=0, max_digits=9, decimal_places=6)),
                ('latitude', models.DecimalField(default=0, max_digits=9, decimal_places=6)),
                ('address', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=63, blank=True)),
                ('state', models.CharField(blank=True, max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip_code', models.CharField(max_length=6, null=True)),
                ('fed_district', models.CharField(default=None, max_length=63, null=True)),
                ('state_district', models.CharField(default=None, max_length=63, null=True)),
                ('beta_access', models.BooleanField(default=False)),
                ('full_account', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(default=b'profile/default.png', null=True, upload_to=api.models.account.PathAndRename(b'profile/'), blank=True)),
            ],
        ),

        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Civi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('body', models.CharField(max_length=4095)),
                ('c_type', models.CharField(default=b'problem', max_length=31, choices=[(b'problem', b'Problem'), (b'cause', b'Cause'), (b'solution', b'Solution')])),
                # ('votes_vneg', models.IntegerField(default=0)),
                # ('votes_neg', models.IntegerField(default=0)),
                # ('votes_neutral', models.IntegerField(default=0)),
                # ('votes_pos', models.IntegerField(default=0)),
                # ('votes_vpos', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),

            ],
        ),
        migrations.AddField(
            model_name='civi',
            name='votes_neutral',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),


        migrations.CreateModel(
            name='Rebuttal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(max_length=1023)),
                ('votes_vneg', models.IntegerField(default=0)),
                ('votes_neg', models.IntegerField(default=0)),
                ('votes_neutral', models.IntegerField(default=0)),
                ('votes_pos', models.IntegerField(default=0)),
                ('votes_vpos', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),
            ],
        ),

        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('body', models.TextField(max_length=2047)),
                ('votes_vneg', models.IntegerField(default=0)),
                ('votes_neg', models.IntegerField(default=0)),
                ('votes_neutral', models.IntegerField(default=0)),
                ('votes_pos', models.IntegerField(default=0)),
                ('votes_vpos', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(default=None, to='api.Account', null=True, on_delete=models.PROTECT)),
                ('civi', models.ForeignKey(default=None, to='api.Civi', null=True, on_delete=models.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='rebuttal',
            name='response',
            field=models.ForeignKey(default=None, to='api.Response', null=True, on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='civi',
            name='hashtags',
            field=models.ManyToManyField(to='api.Hashtag'),
        ),

        migrations.AddField(
            model_name='account',
            name='ai_interests',
            field=models.ManyToManyField(related_name='ai_interests', to='api.Hashtag'),
        ),
        migrations.AddField(
            model_name='account',
            name='followers',
            field=models.ManyToManyField(related_name='_account_followers_+', to='api.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='_account_following_+', to='api.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='interests',
            field=models.ManyToManyField(related_name='interests', to='api.Hashtag'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT),
        ),
    ]
