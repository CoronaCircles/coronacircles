# Generated by Django 3.0.6 on 2020-05-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0016_event_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participation',
            options={'verbose_name': 'Participation', 'verbose_name_plural': 'Participations'},
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='body_template',
            field=models.TextField(help_text='Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }}, {{ event.delete_url }} etc. can be used. Also: {{ leave_url }}', verbose_name='Body Template'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='body_template_de',
            field=models.TextField(help_text='Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }}, {{ event.delete_url }} etc. can be used. Also: {{ leave_url }}', null=True, verbose_name='Body Template'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='body_template_en',
            field=models.TextField(help_text='Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }}, {{ event.delete_url }} etc. can be used. Also: {{ leave_url }}', null=True, verbose_name='Body Template'),
        ),
    ]
