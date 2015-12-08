# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0007_auto_20151017_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
    ]
