# Generated by Django 4.1.6 on 2023-10-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        blank=True, null=True, verbose_name="Language Name"
                    ),
                ),
                (
                    "code2",
                    models.TextField(
                        blank=True, null=True, verbose_name="Language code 2"
                    ),
                ),
            ],
            options={
                "verbose_name": "Idioma",
                "verbose_name_plural": "Languages",
            },
        ),
    ]
