# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
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
    ]
