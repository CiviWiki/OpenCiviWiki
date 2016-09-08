# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160809_0533'),
    ]

    operations = [
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
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(default=b'new_follower', max_length=31, choices=[(b'new_follower', b'New follower'), (b'response_to_yout_civi', b'Response to your civi'), (b'rebuttal_to_your_response', b'Rebuttal to your response')])),
                ('read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
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
                ('bill', models.ForeignKey(default=None, to='api.Bill', null=True)),
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
            ],
        ),
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
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(default=b'abstain', max_length=31, choices=[(b'yes', b'Yes'), (b'no', b'No'), (b'abstain', b'Abstain')])),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('bill', models.ForeignKey(default=None, to='api.Bill', null=True)),
                ('representative', models.ForeignKey(default=None, to='api.Representative', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='civi',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='civi',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='creator',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_negative1',
            new_name='votes_neg',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_positive1',
            new_name='votes_pos',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_negative2',
            new_name='votes_vneg',
        ),
        migrations.RenameField(
            model_name='civi',
            old_name='votes_positive2',
            new_name='votes_vpos',
        ),
        migrations.RenameField(
            model_name='response',
            old_name='creator',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='response',
            old_name='votes_negative1',
            new_name='votes_neg',
        ),
        migrations.RenameField(
            model_name='response',
            old_name='votes_positive1',
            new_name='votes_pos',
        ),
        migrations.RenameField(
            model_name='response',
            old_name='votes_negative2',
            new_name='votes_vneg',
        ),
        migrations.RenameField(
            model_name='response',
            old_name='votes_positive2',
            new_name='votes_vpos',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='topic',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='account',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='account',
            name='award_list',
        ),
        migrations.RemoveField(
            model_name='account',
            name='city',
        ),
        migrations.RemoveField(
            model_name='account',
            name='civi_history',
        ),
        migrations.RemoveField(
            model_name='account',
            name='civi_pins',
        ),
        migrations.RemoveField(
            model_name='account',
            name='country',
        ),
        migrations.RemoveField(
            model_name='account',
            name='cover_image',
        ),
        migrations.RemoveField(
            model_name='account',
            name='friend_requests',
        ),
        migrations.RemoveField(
            model_name='account',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='account',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='account',
            name='statistics',
        ),
        migrations.RemoveField(
            model_name='account',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='bill_against',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='bill_for',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='bill_source',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='response',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='sources',
        ),
        migrations.RemoveField(
            model_name='civi',
            name='visits',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='title',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='votes_negative1',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='votes_negative2',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='votes_neutral',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='votes_positive1',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='votes_positive2',
        ),
        migrations.RemoveField(
            model_name='response',
            name='sources',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='cause',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='bill',
        ),
        migrations.AddField(
            model_name='account',
            name='ai_interests',
            field=models.ManyToManyField(related_name='ai_interests', to='api.Hashtag'),
        ),
        migrations.AddField(
            model_name='account',
            name='fed_district',
            field=models.CharField(default=None, max_length=63, null=True),
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
            name='state_district',
            field=models.CharField(default=None, max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='c_type',
            field=models.CharField(default=b'problem', max_length=31, choices=[(b'problem', b'Problem'), (b'cause', b'Cause'), (b'solution', b'Solution')]),
        ),
        migrations.AddField(
            model_name='civi',
            name='children',
            field=models.ManyToManyField(related_name='_civi_children_+', to='api.Civi'),
        ),
        migrations.AddField(
            model_name='civi',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='parents',
            field=models.ManyToManyField(related_name='_civi_parents_+', to='api.Civi'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='name',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='response',
            name='civi',
            field=models.ForeignKey(default=None, to='api.Civi', null=True),
        ),
        migrations.AddField(
            model_name='response',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='response',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(default=None, to='api.Account', null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='hashtags',
            field=models.ManyToManyField(to='api.Hashtag'),
        ),
        migrations.AddField(
            model_name='thread',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.RemoveField(
            model_name='account',
            name='interests',
        ),
        migrations.AddField(
            model_name='account',
            name='interests',
            field=models.ManyToManyField(related_name='interests', to='api.Hashtag'),
        ),
        migrations.AlterField(
            model_name='account',
            name='zip_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='civi',
            name='body',
            field=models.CharField(max_length=4095),
        ),
        migrations.AlterField(
            model_name='civi',
            name='title',
            field=models.CharField(max_length=127),
        ),
        migrations.AlterField(
            model_name='response',
            name='body',
            field=models.TextField(max_length=2047),
        ),
        migrations.AlterField(
            model_name='response',
            name='title',
            field=models.CharField(max_length=127),
        ),
        migrations.RemoveField(
            model_name='thread',
            name='facts',
        ),
        migrations.AlterField(
            model_name='topic',
            name='category',
            field=models.ForeignKey(default=None, to='api.Category', null=True),
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AddField(
            model_name='representative',
            name='account',
            field=models.ForeignKey(default=None, to='api.Account', null=True),
        ),
        migrations.AddField(
            model_name='rebuttal',
            name='author',
            field=models.ForeignKey(default=None, to='api.Account', null=True),
        ),
        migrations.AddField(
            model_name='rebuttal',
            name='response',
            field=models.ForeignKey(default=None, to='api.Response', null=True),
        ),
        migrations.AddField(
            model_name='rationale',
            name='representative',
            field=models.ForeignKey(default=None, to='api.Representative', null=True),
        ),
        migrations.AddField(
            model_name='rationale',
            name='vote',
            field=models.ForeignKey(default=None, to='api.Vote', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='account',
            field=models.ForeignKey(default=None, to='api.Account', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='civi',
            field=models.ForeignKey(default=None, to='api.Civi', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='thread',
            field=models.ForeignKey(default=None, to='api.Thread', null=True),
        ),
        migrations.AddField(
            model_name='civi',
            name='bill',
            field=models.ForeignKey(default=None, to='api.Bill', null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='facts',
            field=models.ManyToManyField(to='api.Fact'),
        ),
    ]
