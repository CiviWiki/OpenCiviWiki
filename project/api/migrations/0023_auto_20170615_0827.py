# -*- coding: utf-8 -*-


from django.db import migrations, models
import api.models.account


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20170531_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image_thumb',
            field=models.ImageField(null=True, upload_to=api.models.account.PathAndRename(b''), blank=True),
        ),
    ]
