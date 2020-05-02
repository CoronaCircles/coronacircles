import uuid
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template import Template, Context
from django.core import mail


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

    def __str__(self) -> str:
        return str(self.start)

    def mail_participants(self):
        """Sends mails to all participants including host with the join url"""
        addrs = [p.email for p in self.participants.all()] + [self.host.email]
        messages = []
        for addr in addrs:
            messages.append(
                (
                    "You are participating in a CoronaCircle",
                    f"Your circle is starting on {self.start}. Click here to join the circle: {self.join_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [addr],
                )
            )
        send_mass_mail(messages)
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
    language_code = models.CharField(_("Language Code"), max_length=255)

    subject_template = models.CharField(_("Subject Template"), max_length=255)
    body_template = models.TextField(_("Body Template"))

    def __str__(self) -> str:
        return self.choices

    def render(self, context, to_email, connection=None) -> mail.EmailMessage:
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
    def get_mails(
        cls, type, language_code, context, to_emails, connection=None
    ) -> [mail.EmailMessage]:
        """get multiple emails from template for type and language to all to_emails"""
        try:
            template = cls.objects.get(type=type, language_code=language_code)
        except cls.DoesNotExist:
            try:
                template = cls.objects.get(type=type, language_code="en")
            except cls.DoesNotExist:
                return []

        emails = []
        for to_email in to_emails:
            emails.append(
                template.render(
                    context=context, to_email=to_email, connection=connection
                )
            )

        return emails

    @classmethod
    def send_mails(cls, type, language_code, context, to_emails):
        """send multiple emails using one connection"""
        with mail.get_connection() as connection:
            for email in cls.get_mails(
                type=type,
                language_code=language_code,
                context=context,
                to_emails=to_emails,
                connection=connection,
            ):
                email.send(fail_silently=True)
