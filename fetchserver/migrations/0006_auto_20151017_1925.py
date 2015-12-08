# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0005_auto_20151002_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('is_deleted', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userdetails',
            unique_together=set([('user_id', 'password', 'email')]),
        ),
        migrations.AlterIndexTogether(
            name='userdetails',
            index_together=set([('email', 'password')]),
        ),
    ]
