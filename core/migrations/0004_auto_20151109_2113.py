# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_recommendation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recommendation',
            old_name='text',
            new_name='recommendation',
        ),
    ]
