# Generated by Django 4.1.6 on 2023-07-13 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("usefulmodels", "0011_auto_20221108_2356"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Criador",
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Atualizador",
            ),
        ),
        migrations.AlterField(
            model_name="city",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Criador",
            ),
        ),
        migrations.AlterField(
            model_name="city",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Atualizador",
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Criador",
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Atualizador",
            ),
        ),
        migrations.AlterField(
            model_name="practice",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Criador",
            ),
        ),
        migrations.AlterField(
            model_name="practice",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Atualizador",
            ),
        ),
        migrations.AlterField(
            model_name="state",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Criador",
            ),
        ),
        migrations.AlterField(
            model_name="state",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Atualizador",
            ),
        ),
        migrations.AlterField(
            model_name="thematicarea",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Criador",
            ),
        ),
        migrations.AlterField(
            model_name="thematicarea",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Atualizador",
            ),
        ),
    ]
