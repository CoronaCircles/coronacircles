import uuid
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.conf import settings


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
    start = models.DateTimeField(_("Date"))

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
                    _("You are participating in a CoronaCircle"),
                    f_("Your circle is starting on {self.start}. Click here to join the circle: {self.join_url}"),
                    settings.DEFAULT_FROM_EMAIL,
                    [addr],
                )
            )
        send_mass_mail(messages)
        self.mails_sent = True
        self.save()

    class Meta:
        ordering = ("start",)
