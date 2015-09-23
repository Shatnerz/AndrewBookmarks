# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='description',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
