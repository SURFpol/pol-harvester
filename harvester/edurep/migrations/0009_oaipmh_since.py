# Generated by Django 2.2.10 on 2020-03-05 10:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('edurep', '0008_improved_harvest'),
    ]

    operations = [
        migrations.AddField(
            model_name='edurepoaipmh',
            name='since',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
