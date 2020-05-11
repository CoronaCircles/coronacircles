# Generated by Django 3.0.6 on 2020-05-07 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0019_event_tzname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtemplate',
            name='body_template',
            field=models.TextField(help_text='Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }}, {{ event.delete_url }} etc. can be used. Also: {{ leave_url }} for join template only. Note that all datetimes are evaluated in the timezone of the event.', verbose_name='Body Template'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='body_template_de',
            field=models.TextField(help_text='Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }}, {{ event.delete_url }} etc. can be used. Also: {{ leave_url }} for join template only. Note that all datetimes are evaluated in the timezone of the event.', null=True, verbose_name='Body Template'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='body_template_en',
            field=models.TextField(help_text='Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }}, {{ event.delete_url }} etc. can be used. Also: {{ leave_url }} for join template only. Note that all datetimes are evaluated in the timezone of the event.', null=True, verbose_name='Body Template'),
        ),
    ]