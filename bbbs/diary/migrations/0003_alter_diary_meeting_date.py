# Generated by Django 3.2.5 on 2021-08-13 18:40

import bbbs.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20210812_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='meeting_date',
            field=models.DateField(validators=[bbbs.common.validators.year_validator], verbose_name='meeting date'),
        ),
    ]
