import datetime
import pytz

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from circles.models import Event

User = get_user_model()


class EventHostTestCase(TestCase):
    url = reverse("circles:host")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Neues Event erstellen", status_code=200)

    def test_post(self):
        response = self.client.post(
            self.url,
            {"start": "5.1.2020 20:00", "email": "max@mustermann.com",},
            follow=True,
        )
        self.assertRedirects(response, "/hosted")
        self.assertContains(response, "Dein Event wurde erstellt.")

        # user and event were created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.get()
        # user was added as host
        self.assertEqual(event.host.email, "max@mustermann.com")

    # TODO: Test for existing user


class EventJoinTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        self.event = Event(
            host=self.host, start=datetime.datetime(2020, 5, 1, 20, 0, tzinfo=pytz.UTC)
        )
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
        self.assertContains(response, "1. Mai 2020")
