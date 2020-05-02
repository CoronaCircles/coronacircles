import datetime
import pytz

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

from circles.models import Event, MailTemplate

User = get_user_model()


class EventTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()

        self.event = Event(
            host=self.host, start=datetime.datetime(2020, 5, 1, 20, 0, tzinfo=pytz.UTC)
        )
        self.event.save()

    def test_is_past(self):
        event = Event(
            host=self.host, start=datetime.datetime(1999, 5, 1, 20, 0, tzinfo=pytz.UTC)
        )
        self.assertTrue(event.is_past)

    def test_is_full(self):
        self.assertFalse(self.event.is_full)
        # create 6 participants
        for i in range(1, 7):
            email = f"test{i}@example.com"
            user = User(email=email, username=email)
            user.save()
            self.event.participants.add(user)
        self.event.save()
        self.assertTrue(self.event.is_full)

    def test_ical(self):
        self.assertEqual(
            self.event.ical,
            b"BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nSUMMARY:Corona Circle\r\nDTSTART;VALUE=DATE-TIME:20200501T200000Z\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n",
        )


class EventQuerySetTestCase(TestCase):
    def test_upcoming(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        Event(
            host=self.host, start=datetime.datetime(1999, 5, 1, 20, 0, tzinfo=pytz.UTC)
        ).save()
        Event(
            host=self.host, start=datetime.datetime(2222, 5, 1, 20, 0, tzinfo=pytz.UTC)
        ).save()
        self.assertEqual(Event.objects.upcoming().count(), 1)


class MailTemplateTestCase(TestCase):
    def setUp(self):
        self.template = MailTemplate(
            type="join_confirmation",
            language_code="de",
            subject_template="Event beigetreten",
            body_template="{{ testvariable }}",
        )
        self.template.save()

    def test_render(self):
        mail = self.template.render(
            {"testvariable": "This is a test"}, "max@example.com"
        )
        self.assertEqual(mail.body, "This is a test")
        self.assertEqual(mail.subject, "Event beigetreten")
        self.assertEqual(mail.to, ["max@example.com"])

    def test_get_mail(self):
        mail = MailTemplate.get_mail(
            "join_confirmation",
            "de",
            {"testvariable": "This is a test"},
            "max@example.com",
        )
        self.assertEqual(mail.subject, "Event beigetreten")
