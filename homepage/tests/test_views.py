from django.urls import reverse
from django.test import TestCase

from homepage.models import SimplePage


class HomepageTestCase(TestCase):
    url = reverse("homepage:index")

    def test_get(self):
        """Just check the page renders without errors"""
        response = self.client.get(self.url)
        self.assertContains(response, "", status_code=200)


class SimplePageViewTestCase(TestCase):
    def setUp(self):
        self.page = SimplePage(url="test", title="test", text="This is a test")
        self.page.save()
        self.url = reverse("homepage:page", args=["test"])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "This is a test", status_code=200)
