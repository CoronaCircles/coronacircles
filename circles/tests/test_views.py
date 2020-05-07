import datetime
import pytz

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core import mail

from circles.models import Event, MailTemplate, Participation

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
        self.assertContains(response, "Upcoming Circles", status_code=200)
        # only upcoming events
        self.assertEqual(response.context["events"].count(), 1)


class EventHostTestCase(TestCase):
    url = reverse("circles:host")

    def setUp(self):
        self.tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Host a circle", status_code=200)

    def test_post(self):
        # mail template
        MailTemplate(
            type="host_confirmation", subject_template="test", body_template="test",
        ).save()

        response = self.client.post(
            self.url,
            {"start": self.tomorrow, "email": "max@mustermann.com", "language": "en"},
        )
        self.assertContains(response, "was created", status_code=200)

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
        self.assertContains(response, "Has to be in the future", status_code=200)

    def test_can_get_delete_url(self):
        MailTemplate(
            type="host_confirmation",
            subject_template="test",
            body_template="{{ event.delete_url }}",
        ).save()

        self.client.post(
            self.url,
            {"start": self.tomorrow, "email": "max@mustermann.com", "language": "en"},
        )
        event = Event.objects.get()

        self.assertEqual(mail.outbox[0].body, event.delete_url)


class EventJoinTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        self.tomorrow = timezone.now() + datetime.timedelta(days=1)
        self.event = Event(host=self.host, start=self.tomorrow)
        self.event.save()
        self.url = reverse("circles:participate", args=[self.event.pk])

        # mail template
        MailTemplate(
            type="join_confirmation", subject_template="test", body_template="test",
        ).save()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Participate in circle", status_code=200)

    def test_post(self):
        response = self.client.post(self.url, {"email": "max@mustermann.com",})
        self.assertContains(response, "You are participating", status_code=200)

        # user is added as participant
        self.assertEqual(self.event.participants.count(), 1)
        self.assertEqual(self.event.participants.get().email, "max@mustermann.com")

        # email is sent
        self.assertEqual(len(mail.outbox), 1)

    def test_post_event_past(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        past_event = Event(host=self.host, start=yesterday)
        past_event.save()
        url = reverse("circles:participate", args=[past_event.pk])

        response = self.client.post(url, {"email": "max@mustermann.com",})
        self.assertContains(response, "You can not join", status_code=400)

    def test_post_same_user_twice(self):
        """Test that a user is not added twice as participant"""
        self.client.post(self.url, {"email": "max@mustermann.com"})
        self.client.post(self.url, {"email": "max@mustermann.com"})
        self.assertEqual(self.event.participants.count(), 1)

    def test_can_get_leave_url(self):
        template = MailTemplate.objects.get()
        template.body_template = "{{ leave_url }}"
        template.save()

        self.client.post(
            self.url, {"start": self.tomorrow, "email": "max@mustermann.com"},
        )
        participation = Participation.objects.get()

        self.assertEqual(mail.outbox[0].body, participation.leave_url)


class EventDeleteTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        self.tomorrow = timezone.now() + datetime.timedelta(days=1)
        self.event = Event(host=self.host, start=self.tomorrow)
        self.event.save()

        # add participant
        user, _ = User.objects.get_or_create(
            email="max@mustermann.com", username="max@mustermann.com"
        )
        self.event.participants.add(user)
        self.event.save()

        self.url = reverse("circles:delete", args=[self.event.uuid])

        # mail template
        MailTemplate(
            type="deleted", subject_template="test", body_template="test",
        ).save()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Delete circle", status_code=200)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, "/", target_status_code=302)

        # event was deleted
        self.assertEqual(Event.objects.all().count(), 0)

        # mail sent to participants and host
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ["max@mustermann.com"])


class EventLeaveViewTestCase(TestCase):
    def setUp(self):
        self.host = User(email="host@example.com", username="host@example.com")
        self.host.save()
        self.tomorrow = timezone.now() + datetime.timedelta(days=1)
        self.event = Event(host=self.host, start=self.tomorrow)
        self.event.save()

        # add participant
        user, _ = User.objects.get_or_create(
            email="max@mustermann.com", username="max@mustermann.com"
        )
        self.participation = Participation.objects.create(event=self.event, user=user)

        self.url = reverse("circles:leave", args=[self.participation.uuid])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Leave circle", status_code=200)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, "/", target_status_code=302)

        # Participation was deleted
        self.assertEqual(Participation.objects.all().count(), 0)
