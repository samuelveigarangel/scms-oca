# Generated by Django 3.2.12 on 2022-09-14 10:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event_directory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventdirectory",
            name="record_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", ""),
                    ("WIP", "WIP"),
                    ("TO MODERATE", "TO MODERATE"),
                    ("PUBLISHED", "PUBLISHED"),
                ],
                max_length=255,
                null=True,
                verbose_name="Record status",
            ),
        ),
    ]
