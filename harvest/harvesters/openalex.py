import gzip
import io
import json
import logging
import re
from datetime import date

from django.conf import settings
from django.utils import timezone

from core.utils.utils import fetch_data
from harvest.exception_logs import ExceptionContext
from harvest.harvesters.common import JSON_HEADERS
from harvest.models import (
    HarvestErrorLogOpenAlex,
    HarvestStatus,
    OpenAlexHarvestRequest,
    OpenAlexRequestKind,
)

logger = logging.getLogger(__name__)

S3_BUCKET_PREFIX = "s3://openalex/"
UPDATED_DATE_RE = re.compile(r"updated_date=(\d{4}-\d{2}-\d{2})")


def s3_url_to_https(s3_url):
    return (
        f"{settings.OPENALEX_SNAPSHOT_BASE_URL.rstrip('/')}/"
        f"{s3_url.removeprefix(S3_BUCKET_PREFIX)}"
    )


def parse_updated_date_from_url(url):
    return date.fromisoformat(UPDATED_DATE_RE.search(url).group(1))


def iter_part_files(manifest, from_updated_date):
    """
    Lista e ordena as parts do manifest elegíveis para coleta.

    Filtra entradas com ``updated_date`` maior ou igual a ``from_updated_date``
    e enriquece cada item com URL HTTPS e metadados do manifest.

    Parâmetros:
        manifest (dict): Conteúdo JSON do manifest OpenAlex (``date`` + ``files``).
        from_updated_date (str ou date): Data mínima da partição a considerar.

    Retorna:
        list[dict]: Parts ordenadas por ``updated_date`` e URL, cada uma com
        ``s3_url``, ``https_url``, ``updated_date`` e ``record_count``.
    """
    from_date = date.fromisoformat(str(from_updated_date))
    parts = [
        {
            "s3_url": entry["url"],
            "https_url": s3_url_to_https(entry["url"]),
            "updated_date": parse_updated_date_from_url(entry["url"]),
            "record_count": entry["meta"]["record_count"],
        }
        for entry in manifest["files"]
        if parse_updated_date_from_url(entry["url"]) >= from_date
    ]
    return sorted(parts, key=lambda part: (part["updated_date"], part["https_url"]))


def fetch_part_document_ids(url, publication_year_from, is_xpac):
    """
    Baixa uma part gzip/JSONL e retorna os IDs OpenAlex que passam nos filtros.

    Não persiste o payload completo dos works — apenas os IDs que atendem a
    ``publication_year >= publication_year_from`` e, quando informado, ao filtro
    ``is_xpac``.

    Parâmetros:
        url (str): URL HTTPS da part no snapshot S3.
        publication_year_from (int): Ano mínimo de publicação.
        is_xpac (bool ou None): Quando definido, exige ``work["is_xpac"]`` igual
            a este valor; ``None`` desativa o filtro.

    Retorna:
        list[str]: IDs OpenAlex (ex.: ``https://openalex.org/W123``).
    """
    payload = fetch_data(
        url,
        headers=JSON_HEADERS,
        json=False,
        timeout=settings.OPENALEX_PART_FETCH_TIMEOUT,
        verify=True,
    )
    document_ids = []
    with gzip.GzipFile(fileobj=io.BytesIO(payload)) as gzip_file:
        for line in gzip_file:
            work = json.loads(line)
            publication_year = work.get("publication_year")
            if publication_year is None or publication_year < publication_year_from:
                continue
            if is_xpac is not None and work.get("is_xpac", False) is not is_xpac:
                continue
            document_ids.append(work["id"])
    return document_ids


def fetch_manifest(user, publication_year_from, is_xpac):
    """
    Busca o manifest de works do snapshot OpenAlex.

    Em caso de falha na requisição, registra ``OpenAlexHarvestRequest`` e log de
    erro, sem relançar a exceção.

    Parâmetros:
        user: Usuário responsável pela coleta (campo ``creator``).
        publication_year_from (int): Ano mínimo usado nos registros de log.
        is_xpac (bool ou None): Valor do filtro ``is_xpac`` usado nos registros.

    Retorna:
        dict ou None: Manifest JSON em sucesso; ``None`` se a requisição falhar.
    """
    try:
        return fetch_data(
            settings.OPENALEX_WORKS_MANIFEST_URL,
            headers=JSON_HEADERS,
            json=True,
            timeout=60,
            verify=True,
        )
    except Exception as exc:
        logger.error(f"Erro ao buscar manifest OpenAlex: {exc}")
        manifest_request = OpenAlexHarvestRequest.objects.create(
            creator=user,
            request_url=settings.OPENALEX_WORKS_MANIFEST_URL,
            request_kind=OpenAlexRequestKind.MANIFEST,
            publication_year_from=publication_year_from,
            is_xpac=is_xpac,
            harvest_status=HarvestStatus.IN_PROGRESS,
            requested_at=timezone.now(),
        )
        manifest_error = ExceptionContext(
            harvest_object=manifest_request,
            log_model=HarvestErrorLogOpenAlex,
            fk_field="openalex_request",
        )
        manifest_error.add_exception(
            exception=exc,
            field_name="manifest",
            context_data={"url": settings.OPENALEX_WORKS_MANIFEST_URL},
        )
        manifest_error.save_to_db()
        manifest_error.mark_status_harvest()
        return None


def process_part(part, user, publication_year_from, is_xpac):
    """
    Coleta uma part do snapshot e persiste o log da requisição.

    Cria ``OpenAlexHarvestRequest`` (kind ``part``), baixa os IDs filtrados,
    atualiza ``document_ids`` e ``result_count``, e marca sucesso ou falha.

    Parâmetros:
        part (dict): Item retornado por ``iter_part_files``.
        user: Usuário responsável pela coleta.
        publication_year_from (int): Ano mínimo de publicação.
        is_xpac (bool ou None): Filtro opcional de works curados XPAC.

    Retorna:
        bool: ``True`` se a part foi coletada com sucesso; ``False`` em erro.
    """
    part_request = OpenAlexHarvestRequest.objects.create(
        creator=user,
        request_url=part["https_url"],
        request_kind=OpenAlexRequestKind.PART,
        updated_date=part["updated_date"],
        publication_year_from=publication_year_from,
        is_xpac=is_xpac,
        manifest_record_count=part["record_count"],
        harvest_status=HarvestStatus.IN_PROGRESS,
        requested_at=timezone.now(),
    )
    try:
        part_request.document_ids = fetch_part_document_ids(
            part["https_url"],
            publication_year_from,
            is_xpac,
        )
        part_request.result_count = len(part_request.document_ids)
        part_request.save(update_fields=["document_ids", "result_count", "updated"])
        part_request.mark_as_success()
        logger.info(
            f"Part coletada: {part['https_url']} "
            f"({part_request.result_count} IDs com "
            f"publication_year>={publication_year_from})"
        )
        return True
    except Exception as exc:
        logger.error(f"Erro ao buscar part OpenAlex {part['https_url']}: {exc}")
        part_error = ExceptionContext(
            harvest_object=part_request,
            log_model=HarvestErrorLogOpenAlex,
            fk_field="openalex_request",
        )
        part_error.add_exception(
            exception=exc,
            field_name="part",
            context_data={"url": part["https_url"]},
        )
        part_error.save_to_db()
        part_error.mark_status_harvest()
        return False


def process_manifest_parts(
    manifest_request,
    parts,
    user,
    publication_year_from,
    is_xpac,
    max_parts,
):
    """
    Processa as parts pendentes de um manifest já registrado.

    Pula URLs com coleta anterior em ``success``. Interrompe e marca o manifest
    como ``failed`` na primeira part com erro. Marca o manifest como ``success``
    somente quando todas as parts elegíveis estão concluídas.

    Parâmetros:
        manifest_request (OpenAlexHarvestRequest): Registro do manifest em andamento.
        parts (iterable): Parts retornadas por ``iter_part_files``.
        user: Usuário responsável pela coleta.
        publication_year_from (int): Ano mínimo de publicação.
        is_xpac (bool ou None): Filtro opcional de works curados XPAC.
        max_parts (int ou None): Limite de parts a processar nesta execução;
            ``None`` processa todas as pendentes.
    """
    completed_urls = OpenAlexHarvestRequest.get_completed_part_urls()
    processed = 0

    for part in parts:
        if max_parts is not None and processed >= max_parts:
            break

        if part["https_url"] in completed_urls:
            logger.info(
                f"Part já coletada com sucesso, pulando: {part['https_url']}"
            )
            continue

        if not process_part(part, user, publication_year_from, is_xpac):
            manifest_request.mark_as_failed()
            return

        completed_urls.add(part["https_url"])
        processed += 1

    manifest_completed = all(
        part["https_url"] in completed_urls
        for part in parts
    )
    if manifest_completed:
        manifest_request.mark_as_success()


def harvest_openalex_works(
    user,
    publication_year_from,
    from_updated_date,
    max_parts=None,
    is_xpac=None,
):
    """
    Orquestra a coleta incremental do snapshot OpenAlex (works).

    Fluxo: busca manifest → verifica se já foi processado → registra manifest →
    coleta parts pendentes desde ``from_updated_date``, aplicando filtros de ano
    e ``is_xpac``. Não indexa no OpenSearch nesta etapa.

    Parâmetros:
        user: Usuário responsável pela coleta.
        publication_year_from (int): Ano mínimo de publicação dos works.
        from_updated_date (str ou date): Data mínima das parts S3 a considerar.
        max_parts (int ou None, opcional): Limite de parts por execução.
        is_xpac (bool ou None, opcional): Filtro de works curados XPAC.
    """
    logger.info(
        f"Iniciando coleta OpenAlex snapshot a partir de {from_updated_date}, "
        f"publication_year>={publication_year_from}, is_xpac={is_xpac}"
    )

    manifest = fetch_manifest(user, publication_year_from, is_xpac)
    if manifest is None:
        return

    manifest_date = date.fromisoformat(manifest["date"])
    manifest_processed = OpenAlexHarvestRequest.objects.filter(
        request_kind=OpenAlexRequestKind.MANIFEST,
        updated_date=manifest_date,
        harvest_status=HarvestStatus.SUCCESS,
    ).exists()
    if manifest_processed:
        logger.info(f"Manifest OpenAlex {manifest_date} já processado.")
        return

    manifest_request = OpenAlexHarvestRequest.objects.create(
        creator=user,
        request_url=settings.OPENALEX_WORKS_MANIFEST_URL,
        request_kind=OpenAlexRequestKind.MANIFEST,
        updated_date=manifest_date,
        publication_year_from=publication_year_from,
        is_xpac=is_xpac,
        harvest_status=HarvestStatus.IN_PROGRESS,
        requested_at=timezone.now(),
    )
    process_manifest_parts(
        manifest_request=manifest_request,
        parts=iter_part_files(manifest, from_updated_date),
        user=user,
        publication_year_from=publication_year_from,
        is_xpac=is_xpac,
        max_parts=max_parts,
    )
