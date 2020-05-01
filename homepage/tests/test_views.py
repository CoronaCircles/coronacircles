from django.urls import reverse
from django.test import TestCase


class HomepageTestCase(TestCase):
    url = reverse("homepage:index")

    def test_get(self):
        """Just check the page renders without errors"""
        response = self.client.get(self.url)
        self.assertContains(response, "", status_code=200)
