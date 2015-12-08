# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0003_auto_20150913_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageactivetime',
            name='page_content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
