import datetime
import pytz

from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from django.contrib.auth import get_user_model

from circles.models import Event

User = get_user_model()


class CheckSeminarsTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        self.participant = User(
            email="participant@example.com", username="participant@example.com"
        )
        self.participant.save()
        past_event = Event(
            host=self.host, start=datetime.datetime(1999, 5, 1, 20, 0, tzinfo=pytz.UTC)
        )
        past_event.save()
        past_event.participants.add(self.participant)
        Event(
            host=self.host, start=datetime.datetime(2222, 5, 1, 20, 0, tzinfo=pytz.UTC)
        ).save()

    def test_check_mails_sent(self):
        call_command("mail_participants")
        self.assertEqual(len(mail.outbox), 2)

    def test_not_sent_twice(self):
        call_command("mail_participants")
        call_command("mail_participants")
        call_command("mail_participants")
        call_command("mail_participants")
        self.assertEqual(len(mail.outbox), 2)
