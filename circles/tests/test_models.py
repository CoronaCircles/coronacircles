import datetime
import pytz

from django.test import TestCase
from django.contrib.auth import get_user_model

from circles.models import Event

User = get_user_model()


class EventTestCase(TestCase):
    def test_creation(self):
        event = Event(start=datetime.datetime(2020, 5, 1, 20, 0, tzinfo=pytz.UTC))
        event.save()
        self.assertIsNotNone(event.created_at)
        self.assertIsNotNone(event.pk)

    def test_is_full(self):
        event = Event(start=datetime.datetime(2020, 5, 1, 20, 0, tzinfo=pytz.UTC))
        event.save()
        self.assertFalse(event.is_full)

        # create 6 participants
        for i in range(1, 7):
            email = f"test{i}@example.com"
            user = User(email=email, username=email)
            user.save()
            event.participants.add(user)

        event.save()

        self.assertTrue(event.is_full)
