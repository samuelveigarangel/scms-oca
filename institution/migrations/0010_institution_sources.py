# Generated by Django 4.1.6 on 2023-10-15 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("institution", "0009_alter_sourceinstitution_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="institution",
            name="sources",
            field=models.ManyToManyField(
                to="institution.sourceinstitution", verbose_name="Source Institutions"
            ),
        ),
    ]
