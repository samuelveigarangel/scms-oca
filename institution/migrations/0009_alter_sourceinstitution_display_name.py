# Generated by Django 4.1.6 on 2023-07-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("institution", "0008_rename_institutionsource_sourceinstitution_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sourceinstitution",
            name="display_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Display Name"
            ),
        ),
    ]
