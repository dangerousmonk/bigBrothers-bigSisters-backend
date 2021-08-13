# Generated by Django 3.2.5 on 2021-08-13 18:40

import bbbs.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_alter_story_friends_since'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='friends_since',
            field=models.DateField(validators=[bbbs.common.validators.year_validator], verbose_name='friends since'),
        ),
    ]
