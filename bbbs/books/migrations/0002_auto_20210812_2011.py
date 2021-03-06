# Generated by Django 3.2.5 on 2021-08-12 17:11

from django.db import migrations, models

import bbbs.common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_city_options'),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='slug',
        ),
        migrations.AlterField(
            model_name='book',
            name='color',
            field=models.CharField(choices=[('#C8D1FF', 'light blue'), ('#FF8585', 'orange')], help_text='choose color for the book cover', max_length=7, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(help_text='tags appropriate for this book', related_name='books', to='common.Tag', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='book',
            name='url',
            field=models.URLField(help_text='link to read or buy book', verbose_name='book url'),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='add publication year', validators=[bbbs.common.validators.year_validator], verbose_name='publication year'),
        ),
    ]
