# Generated by Django 4.1.6 on 2023-10-30 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0020_alter_sourceconcepts_specific_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sourceconcepts",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="Name of the concept",
                max_length=512,
                null=True,
                verbose_name="Nome",
            ),
        ),
        migrations.AlterField(
            model_name="sourceconcepts",
            name="normalized_name",
            field=models.CharField(
                blank=True,
                help_text="Name of the concept",
                max_length=512,
                null=True,
                verbose_name="Normalized Name",
            ),
        ),
        migrations.AlterField(
            model_name="sourceconcepts",
            name="specific_id",
            field=models.CharField(max_length=255, verbose_name="Specific Id"),
        ),
    ]
