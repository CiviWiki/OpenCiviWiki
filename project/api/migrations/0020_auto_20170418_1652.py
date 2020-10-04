# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0019_auto_20170418_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invitee_email', models.EmailField(default=None, max_length=254)),
                ('verification_code', models.CharField(max_length=31)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('host_user', models.ForeignKey(related_name='hosts', default=None, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)),
                ('invitee_user', models.ForeignKey(related_name='invitees', default=None, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)),
            ],
        ),
    ]
