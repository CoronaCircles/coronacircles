import datetime
import pytz

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core import mail

from circles.models import Event

User = get_user_model()


class EventListTestCase(TestCase):
    url = reverse("circles:list")

    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        Event(
            host=self.host, start=datetime.datetime(1999, 5, 1, 20, 0, tzinfo=pytz.UTC)
        ).save()
        Event(
            host=self.host, start=datetime.datetime(2222, 5, 1, 20, 0, tzinfo=pytz.UTC)
        ).save()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Kommende Events", status_code=200)
        # only upcoming events
        self.assertEqual(response.context["events"].count(), 1)


class EventHostTestCase(TestCase):
    url = reverse("circles:host")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Neues Event erstellen", status_code=200)

    def test_post(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        response = self.client.post(
            self.url, {"start": tomorrow, "email": "max@mustermann.com",},
        )
        self.assertContains(response, "wurde erstellt.", status_code=200)

        # user and event were created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.get()

        # user was added as host
        self.assertEqual(event.host.email, "max@mustermann.com")

        # email is sent
        self.assertEqual(len(mail.outbox), 1)

    # TODO: Test for existing user

    def test_post_past_date(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        response = self.client.post(
            self.url, {"start": yesterday, "email": "max@mustermann.com",},
        )
        self.assertContains(response, "Muss in der Zukunft sein", status_code=200)


class EventJoinTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        self.event = Event(host=self.host, start=tomorrow)
        self.event.save()
        self.url = reverse("circles:join", args=[self.event.pk])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "teilnehmen", status_code=200)

    def test_post(self):
        response = self.client.post(self.url, {"email": "max@mustermann.com",})
        self.assertContains(
            response, "Du wurdest als Teilnehmer/in eingetragen.", status_code=200
        )

        # user is added as participant
        self.assertEqual(self.event.participants.count(), 1)
        self.assertEqual(self.event.participants.get().email, "max@mustermann.com")

        # email is sent
        self.assertEqual(len(mail.outbox), 1)

    def test_post_event_past(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        past_event = Event(host=self.host, start=yesterday)
        past_event.save()
        url = reverse("circles:join", args=[past_event.pk])

        response = self.client.post(url, {"email": "max@mustermann.com",})
        self.assertContains(response, "Du kannst nicht beitreten.", status_code=400)

    def test_post_same_user_twice(self):
        """Test that a user is not added twice as participant"""
        self.client.post(self.url, {"email": "max@mustermann.com"})
        self.client.post(self.url, {"email": "max@mustermann.com"})
        self.assertEqual(self.event.participants.count(), 1)
