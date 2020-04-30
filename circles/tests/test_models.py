import datetime
import pytz

from django.test import TestCase
from django.contrib.auth import get_user_model

from circles.models import Event

User = get_user_model()


class EventTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()

        self.event = Event(
            host=self.host, start=datetime.datetime(2020, 5, 1, 20, 0, tzinfo=pytz.UTC)
        )
        self.event.save()

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
