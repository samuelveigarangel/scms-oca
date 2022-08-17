# Generated by Django 3.2.12 on 2022-08-17 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usefulmodels', '0011_action_pratice'),
        ('event_directory', '0005_eventdirectory_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdirectory',
            name='action',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usefulmodels.action'),
        ),
        migrations.AddField(
            model_name='eventdirectory',
            name='classification',
            field=models.CharField(blank=True, choices=[('', ''), ('encontro', 'encontro'), ('conferência', 'conferência'), ('congresso', 'congresso'), ('workshop', 'workshop'), ('seminário', 'seminário'), ('outros', 'outros')], max_length=255, null=True, verbose_name='Classification'),
        ),
        migrations.AddField(
            model_name='eventdirectory',
            name='pratice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usefulmodels.pratice'),
        ),
    ]
