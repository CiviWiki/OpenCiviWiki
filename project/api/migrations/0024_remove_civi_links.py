# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20170615_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='civi',
            name='links',
        ),
    ]
