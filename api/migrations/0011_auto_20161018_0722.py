# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_account_representatives'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
        migrations.RemoveField(
            model_name='account',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=6),
        ),
        migrations.AddField(
            model_name='account',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='account',
            name='followers',
            field=models.ManyToManyField(related_name='follower', to='api.Account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='followings', to='api.Account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(default=b'/media/profile/happy.png', null=True, upload_to=b'/media/profile', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='state',
            field=models.CharField(blank=True, max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')]),
        ),
    ]
