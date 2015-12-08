# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fetchserver', '0004_pageactivetime_page_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageactivetime',
            name='page_content',
            field=models.TextField(default=''),
        ),
    ]
