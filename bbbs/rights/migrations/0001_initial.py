# Generated by Django 3.2.5 on 2021-08-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_auto_20210808_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Right',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('text', models.TextField(verbose_name='text')),
                ('color', models.CharField(choices=[('#F8D162', 'yellow'), ('#8CDD94', 'green'), ('#FF8585', 'orange'), ('#C8D1FF', 'light blue')], max_length=7, verbose_name='color')),
                ('image', models.ImageField(blank=True, null=True, upload_to='rights/', verbose_name='image')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('tags', models.ManyToManyField(related_name='rights', to='common.Tag', verbose_name='tags')),
            ],
            options={
                'verbose_name': 'Right',
                'verbose_name_plural': 'Rights',
                'ordering': ['-added_at'],
            },
        ),
    ]
