# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListedPages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.CharField(max_length=500)),
                ('base_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PageActiveTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.CharField(max_length=500)),
                ('page_id', models.CharField(max_length=500)),
                ('page_title', models.CharField(max_length=500)),
                ('base_url', models.CharField(max_length=500)),
                ('cumulative_time', models.IntegerField(default=0)),
                ('icon_url', models.CharField(max_length=500)),
                ('last_updated_timestamp', models.DateTimeField(auto_now=True)),
                ('is_active', models.IntegerField(default=1)),
                ('is_deleted', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['last_updated_timestamp'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='pageactivetime',
            unique_together=set([('user_id', 'page_id')]),
        ),
        migrations.AlterIndexTogether(
            name='pageactivetime',
            index_together=set([('user_id', 'page_id', 'page_title', 'last_updated_timestamp')]),
        ),
        migrations.AlterIndexTogether(
            name='blacklistedpages',
            index_together=set([('user_id', 'base_url')]),
        ),
    ]
