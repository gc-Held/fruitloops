# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blacklistedpages',
            unique_together=set([('user_id', 'base_url')]),
        ),
    ]
