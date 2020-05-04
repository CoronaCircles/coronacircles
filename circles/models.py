import uuid
import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template import Template, Context
from django.core import mail

from icalendar import Calendar, Event as IEvent


class EventQuerySet(models.QuerySet):
    def upcoming(self):
        """events that are in the future"""
        return self.filter(start__gte=timezone.now())

    def to_be_mailed(self):
        """events that are to be mailed, because they start very soon"""
        return self.filter(
            mails_sent=False, start__lte=timezone.now() + datetime.timedelta(minutes=10)
        )


class EventManager(models.Manager.from_queryset(EventQuerySet)):
    pass


class Event(models.Model):
    uuid = models.UUIDField(
        _("UUID for meeting-URL"), default=uuid.uuid4,  # editable=False
    )

    created_at = models.DateTimeField(_("Creation Date"), default=timezone.now)
    start = models.DateTimeField(_("Date and Time"))
    language = models.CharField(
        _("Language"), max_length=2, choices=settings.LANGUAGES, default="en"
    )

    mails_sent = models.BooleanField(_("If e-mail has been sent"), default=False)

    host = models.ForeignKey(
        get_user_model(),
        related_name="hosted_events",
        on_delete=models.CASCADE,
        verbose_name=_("Host"),
    )
    participants = models.ManyToManyField(
        get_user_model(), related_name="events", verbose_name=_("Participants")
    )

    objects = EventManager()

    @property
    def is_full(self) -> bool:
        """determines wether event is already full (6 participants, 7 including host)"""
        return self.participant_count >= 7

    @property
    def is_past(self) -> bool:
        """determines wether event is in the past"""
        return self.start < timezone.now()

    @property
    def participant_count(self) -> int:
        """current number of participants including host"""
        return self.participants.count() + 1

    @property
    def join_url(self) -> str:
        """url to join in Jitsi etc."""
        return f"https://meet.allmende.io/coronacircles-{self.uuid}"

    @property
    def ical(self) -> Calendar:
        """Get ical representation of event"""
        cal = Calendar()
        event = IEvent()
        event.add("summary", "Corona Circle")
        event.add("dtstart", self.start)
        cal.add_component(event)
        return cal.to_ical()

    def __str__(self) -> str:
        return str(self.start)

    def mail_participants(self):
        """Sends mails to all participants including host with the join url"""
        addrs = [p.email for p in self.participants.all()] + [self.host.email]

        with mail.get_connection() as connection:
            for addr in addrs:
                email = MailTemplate.get_mail(
                    type="join",
                    language_code="en",
                    context={"event": self},
                    to_email=addr,
                    connection=connection,
                )
                email.send(fail_silently=True)

        self.mails_sent = True
        self.save()

    class Meta:
        ordering = ("start",)


def render_template(template: str, context: dict) -> str:
    """helper to render a template str with context"""
    if template is None:
        return ""
    return Template(template).render(Context(context))


class MailTemplate(models.Model):
    type = models.CharField(
        _("Type"),
        max_length=255,
        choices=(
            ("join_confirmation", _("Join Confirmation")),
            ("host_confirmation", _("Host Confirmation")),
            ("join", _("Join")),
        ),
    )
    language_code = models.CharField(_("Language Code"), max_length=255, default="en")

    subject_template = models.CharField(
        _("Subject Template"),
        max_length=255,
        help_text=_(
            "Subject of the email to be sent. The Variable {{ event }} and its children {{ event.start }} etc. can be used."
        ),
    )
    body_template = models.TextField(
        _("Body Template"),
        help_text=_(
            "Body text of the email to be sent. The Variable {{ event }} and its children {{ event.start }}, {{ event.join_url }} etc. can be used."
        ),
    )

    def __str__(self) -> str:
        return self.type

    def render(
        self, context: dict, to_email: str, connection=None
    ) -> mail.EmailMessage:
        """render this email template to email message"""
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = render_template(self.subject_template, context)
        body = render_template(self.body_template, context)
        return mail.EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_email.split(","),
            connection=connection,
        )

    @classmethod
    def get_mail(
        cls,
        type: str,
        language_code: str,
        context: dict,
        to_email: str,
        connection=None,
    ) -> mail.EmailMessage:
        """get template and render to email"""
        templates = cls.objects.filter(type=type).filter(
            Q(language_code=language_code) | Q(language_code="en")
        )
        if not templates:
            return None
        return templates[0].render(
            context=context, to_email=to_email, connection=connection
        )
