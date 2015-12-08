# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0002_auto_20150911_2117'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pageactivetime',
            unique_together=set([('user_id', 'page_id', 'last_updated_timestamp')]),
        ),
    ]
