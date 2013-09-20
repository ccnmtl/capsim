from django.test import TestCase
from django.test.client import Client
from capsim.sim.models import RunRecord


class BasicViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_runs(self):
        response = self.c.get("/run/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("<ul>" in response.content)

    def test_run(self):
        rr = RunRecord.objects.create()
        response = self.c.get("/run/%d/" % rr.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("<h2>Saved Run: " in response.content)
