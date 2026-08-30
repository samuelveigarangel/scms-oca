from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("harvest", "0006_globalmetricsuploadfile_stats"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OpenAlexHarvestRequest",
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
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Creation date"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Last update date"),
                ),
                (
                    "request_url",
                    models.TextField(
                        help_text="URL HTTPS efetiva do objeto no snapshot S3",
                        verbose_name="URL da requisição",
                    ),
                ),
                (
                    "request_kind",
                    models.CharField(
                        choices=[
                            ("manifest", "Manifest"),
                            ("part", "Part"),
                        ],
                        db_index=True,
                        max_length=20,
                        verbose_name="Tipo de requisição",
                    ),
                ),
                (
                    "updated_date",
                    models.DateField(
                        blank=True,
                        db_index=True,
                        help_text=(
                            "Data do manifest ou updated_date extraída da URL da partição"
                        ),
                        null=True,
                        verbose_name="Data do manifest ou da partição",
                    ),
                ),
                (
                    "publication_year_from",
                    models.PositiveIntegerField(
                        default=2018,
                        verbose_name="Ano de publicação mínimo",
                    ),
                ),
                (
                    "is_xpac",
                    models.BooleanField(
                        blank=True,
                        help_text=(
                            "Quando definido, coleta apenas works com is_xpac igual a este valor"
                        ),
                        null=True,
                        verbose_name="Filtrar is_xpac",
                    ),
                ),
                (
                    "document_ids",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="IDs OpenAlex dos works com publication_year no filtro",
                        verbose_name="IDs dos documentos",
                    ),
                ),
                (
                    "result_count",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Quantidade de IDs",
                    ),
                ),
                (
                    "manifest_record_count",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="files[].meta.record_count da part no manifest",
                        null=True,
                        verbose_name="Record count do manifest",
                    ),
                ),
                (
                    "harvest_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pendente"),
                            ("in_progress", "Em Progresso"),
                            ("success", "Sucesso"),
                            ("failed", "Falhou"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                        verbose_name="Status da Coleta",
                    ),
                ),
                (
                    "requested_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Requisitado em",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_last_mod_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updater",
                    ),
                ),
            ],
            options={
                "verbose_name": "Requisição OpenAlex",
                "verbose_name_plural": "Requisições OpenAlex",
            },
        ),
        migrations.AddIndex(
            model_name="openalexharvestrequest",
            index=models.Index(
                fields=["request_kind", "harvest_status"],
                name="harvest_ope_request_8a1c2d_idx",
            ),
        ),
        migrations.CreateModel(
            name="HarvestErrorLogOpenAlex",
            fields=[
                (
                    "baseharvesterrorlog_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="harvest.baseharvesterrorlog",
                    ),
                ),
                (
                    "openalex_request",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="harvest_error_log",
                        to="harvest.openalexharvestrequest",
                    ),
                ),
            ],
            bases=("harvest.baseharvesterrorlog",),
        ),
    ]
