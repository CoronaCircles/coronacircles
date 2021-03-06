# Generated by Django 3.0.6 on 2020-05-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20200505_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='URL-Pfad')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('template_name', models.CharField(blank=True, max_length=255, verbose_name='Template Name')),
            ],
            options={
                'verbose_name': 'Simple Page',
                'verbose_name_plural': 'Simple Pages',
                'ordering': ('url',),
            },
        ),
    ]
