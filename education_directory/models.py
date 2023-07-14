import os

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from wagtail.admin.panels import FieldPanel, HelpPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel

from core.models import CommonControlField
from institution.models import Institution
from location.models import Location
from usefulmodels.models import Action, Practice, ThematicArea

from . import choices
from .forms import EducationDirectoryFileForm, EducationDirectoryForm
from .permission_helper import MUST_BE_MODERATE
from core import help_fields



def get_default_action():
    try:
        return Action.objects.get(name__icontains="educa")
    except Action.DoesNotExist:
        return None


class EducationDirectory(CommonControlField):
    class Meta:
        verbose_name_plural = _("Education Data")
        verbose_name= _("Education Data")
        permissions = (
            (MUST_BE_MODERATE, _("Must be moderated")),
            ("can_edit_title", _("Can edit title")),
            ("can_edit_link", _("Can edit link")),
            ("can_edit_description", _("Can edit description")),
            ("can_edit_start_date", _("Can edit start_date")),
            ("can_edit_end_date", _("Can edit end_date")),
            ("can_edit_start_time", _("Can edit start_time")),
            ("can_edit_end_time", _("Can edit end_time")),
            ("can_edit_locations", _("Can edit locations")),
            ("can_edit_institutions", _("Can edit institutions")),
            ("can_edit_thematic_areas", _("Can edit thematic_areas")),
            ("can_edit_practice", _("Can edit practice")),
            ("can_edit_classification", _("Can edit classification")),
            ("can_edit_keywords", _("Can edit keywords")),
            ("can_edit_attendance", _("Can edit attendance")),
            ("can_edit_record_status", _("Can edit record_status")),
            ("can_edit_source", _("Can edit source")),
            (
                "can_edit_institutional_contribution",
                _("Can edit institutional_contribution"),
            ),
            ("can_edit_notes", _("Can edit notes")),
        )

    title = models.CharField(_("Title"), max_length=255, null=False, blank=False, help_text=help_fields.DIRECTORY_TITLE_HELP)
    link = models.URLField(_("Link"), null=False, blank=False, help_text=help_fields.DIRECTORY_LINK_HELP)
    description = models.TextField(
        _("Description"), max_length=1000, null=True, blank=True, help_text=help_fields.DIRECTORY_DESCRIPTION_HELP
    )
    start_date = models.DateField(
        _("Start Date"), max_length=255, null=True, blank=True
    )
    end_date = models.DateField(_("End Date"), max_length=255, null=True, blank=True)
    start_time = models.TimeField(
        _("Start Time"), max_length=255, null=True, blank=True
    )
    end_time = models.TimeField(_("End Time"), max_length=255, null=True, blank=True)

    locations = models.ManyToManyField(Location, verbose_name=_("Location"), blank=False, null=True)
    institutions = models.ManyToManyField(
        Institution, verbose_name=_("Institution"), blank=True, help_text=help_fields.DIRECTORY_INSTITUTIONS_HELP
    )
    thematic_areas = models.ManyToManyField(
        ThematicArea, verbose_name=_("Thematic Area"), blank=True, help_text=help_fields.DIRECTORY_THEMATIC_AREA_HELP
    )


    practice = models.ForeignKey(
        Practice,
        verbose_name=_("Practice"),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text=help_fields.DIRECTORY_PRACTICE_HELP
    )

    action = models.ForeignKey(
        Action,
        verbose_name=_("Action"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=get_default_action,
        help_text=help_fields.DIRECTORY_ACTION_HELP
    )
    classification = models.CharField(
        _("Classification"),
        choices=choices.classification,
        max_length=255,
        null=True,
        blank=True,
        help_text=help_fields.DIRECTORY_CLASSIFICATION_HELP
    )

    keywords = TaggableManager(_("Keywords"), blank=True, help_text=help_fields.DIRECTORY_KEYWORDS_AREA_HELP)


    attendance = models.CharField(
        _("Attendance"),
        choices=choices.attendance_type,
        max_length=255,
        null=True,
        blank=False,
    )

    record_status = models.CharField(
        _("Record status"),
        choices=choices.status,
        max_length=255,
        null=True,
        blank=True,
        help_text=help_fields.DIRECTORY_RECORD_STATUS_HELP
    )


    source = models.CharField(_("Source"), max_length=255, null=True, blank=True, help_text=help_fields.DIRECTORY_SOURCE_HELP)


    institutional_contribution = models.CharField(
        _("Institutional Contribution"),
        max_length=255,
        default=settings.DIRECTORY_DEFAULT_CONTRIBUTOR,
        help_text=help_fields.DIRECTORY_INSTITUTIONAL_CONTRIBUTION_HELP,
    )

    notes = models.TextField(_("Notes"), max_length=1000, null=True, blank=True, help_text=help_fields.DIRECTORY_NOTES_HELP)

    panels = [
        HelpPanel(
            "Cursos livres, disciplinas de graduação e pós-graduação ministrados por instituições brasileiras – presenciais ou EAD- para promover a adoção dos princípios e práticas de ciência aberta por todos os envolvidos no processo de pesquisa."
        ),
        FieldPanel("title", permission="education_directory.can_edit_title"),
        FieldPanel("link", permission="education_directory.can_edit_link"),
        FieldPanel("source", permission="education_directory.can_edit_source"),
        FieldPanel("description", permission="education_directory.can_edit_description"),
        FieldPanel("institutional_contribution", permission="education_directory.can_edit_institutional_contribution"),
        AutocompletePanel("institutions", permission="education_directory.can_edit_institutions"),
        FieldPanel("start_date", permission="education_directory.can_edit_start_date"),
        FieldPanel("end_date", permission="education_directory.can_edit_end_date"),
        FieldPanel("start_time", permission="education_directory.can_edit_start_time"),
        FieldPanel("end_time", permission="education_directory.can_edit_end_time"),
        AutocompletePanel("locations", permission="education_directory.can_edit_locations"),
        AutocompletePanel("thematic_areas", permission="education_directory.can_edit_thematic_areas"),
        FieldPanel("keywords", permission="education_directory.can_edit_keywords"),
        FieldPanel("classification", permission="education_directory.can_edit_classification"),
        FieldPanel("practice", permission="education_directory.can_edit_practice"),
        FieldPanel("attendance", permission="education_directory.can_edit_attendance"),
        FieldPanel("record_status", permission="education_directory.can_edit_record_status"),
        FieldPanel("notes", permission="education_directory.can_edit_notes"),
    ]

    def __unicode__(self):
        return "%s" % self.title

    def __str__(self):
        return "%s" % self.title

    def get_absolute_edit_url(self):
        return f"/education_directory/educationdirectory/edit/{self.id}/"

    @property
    def data(self):
        d = {
            "education__title": self.title,
            "education__link": self.link,
            "education__description": self.description,
            "education__start_date": self.start_date.isoformat() if self.start_date else None,
            "education__end_date": self.end_date.isoformat() if self.end_date else None,
            "education__start_time": self.start_time.isoformat() if self.start_time else None,
            "education__end_time": self.end_time.isoformat() if self.end_time else None,
            "education__classification": self.classification,
            "education__keywords": [keyword for keyword in self.keywords.names()],
            "education__attendance": self.attendance,
            "education__record_status": self.record_status,
            "education__source": self.source,
            "education__institutional_contribution": self.institutional_contribution,
            "education__notes": self.notes,
            "education__action": self.action,
            "education__practice": self.practice,
        }
        if self.locations:
            loc = []
            for location in self.locations.iterator():
                loc.append(location.data)
            d.update({"education__locations": loc})

        if self.institutions:
            inst = []
            for institution in self.institutions.iterator():
                inst.append(institution.data)
            d.update({"education__institutions": inst})

        if self.thematic_areas:
            area = []
            for thematic_area in self.thematic_areas.iterator():
                area.append(thematic_area.data)
            d.update({"education__thematic_areas": area})

        if self.practice:
            d.update(self.practice.data)

        if self.action:
            d.update(self.action.data)

        return d

    base_form_class = EducationDirectoryForm


class EducationDirectoryFile(CommonControlField):
    class Meta:
        verbose_name_plural = _("Education Data Upload")

    attachment = models.ForeignKey(
        "wagtaildocs.Document",
        verbose_name=_("Attachement"),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_valid = models.BooleanField(_("Is valid?"), default=False, blank=True, null=True)
    line_count = models.IntegerField(
        _("Number of lines"), default=0, blank=True, null=True
    )

    def filename(self):
        return os.path.basename(self.attachment.name)

    panels = [FieldPanel("attachment")]
    base_form_class = EducationDirectoryFileForm
