# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_bookmark_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='description',
            field=models.CharField(default=b'Description here', max_length=200),
        ),
    ]
