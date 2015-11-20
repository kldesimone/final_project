# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recommendation_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='location',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
