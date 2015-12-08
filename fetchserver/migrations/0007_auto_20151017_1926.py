# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0006_auto_20151017_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='password',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
    ]
