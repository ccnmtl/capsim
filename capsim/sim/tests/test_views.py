from django.test import TestCase
from django.test.client import Client


class BasicViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_runs(self):
        response = self.c.get("/runs/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("<ul>" in response.content)
