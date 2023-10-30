# Generated by Django 4.1.6 on 2023-10-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0025_alter_concepts_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="concepts",
            field=models.ManyToManyField(
                blank=True, to="article.concepts", verbose_name="Concepts"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="programs",
            field=models.ManyToManyField(
                blank=True, to="article.program", verbose_name="Programs"
            ),
        ),
    ]
