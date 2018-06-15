# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20170331_0710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='civiimage',
            name='last_modified',
        ),
    ]
