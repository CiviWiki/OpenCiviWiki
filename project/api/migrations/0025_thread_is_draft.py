# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_civi_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
