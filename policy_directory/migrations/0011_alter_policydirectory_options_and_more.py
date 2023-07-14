# Generated by Django 4.1.6 on 2023-07-14 16:56

from django.db import migrations, models
import django.db.models.deletion
import policy_directory.models


class Migration(migrations.Migration):

    dependencies = [
        ("usefulmodels", "0012_alter_action_creator_alter_action_updated_by_and_more"),
        ("policy_directory", "0010_alter_policydirectory_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="policydirectory",
            options={
                "permissions": (
                    ("must_be_moderate", "Must be moderated"),
                    ("can_edit_title", "Can edit title"),
                    ("can_edit_link", "Can edit link"),
                    ("can_edit_description", "Can edit description"),
                    ("can_edit_locations", "Can edit locations"),
                    ("can_edit_institutions", "Can edit institutions"),
                    ("can_edit_thematic_areas", "Can edit thematic_areas"),
                    ("can_edit_practice", "Can edit practice"),
                    ("can_edit_classification", "Can edit classification"),
                    ("can_edit_keywords", "Can edit keywords"),
                    ("can_edit_record_status", "Can edit record_status"),
                    ("can_edit_source", "Can edit source"),
                    (
                        "can_edit_institutional_contribution",
                        "Can edit institutional_contribution",
                    ),
                    ("can_edit_notes", "Can edit notes"),
                ),
                "verbose_name": "Policy Data",
                "verbose_name_plural": "Policy Data",
            },
        ),
        migrations.AlterField(
            model_name="policydirectory",
            name="action",
            field=models.ForeignKey(
                blank=True,
                default=policy_directory.models.get_default_action,
                help_text="",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="usefulmodels.action",
                verbose_name="Ação",
            ),
        ),
    ]
