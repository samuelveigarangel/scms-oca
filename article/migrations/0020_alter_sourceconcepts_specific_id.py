# Generated by Django 4.1.6 on 2023-10-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0019_sourceconcepts_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sourceconcepts",
            name="specific_id",
            field=models.CharField(max_length=512, verbose_name="Specific Id"),
        ),
    ]
