from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from capsim.sim.models import RunRecord, RunOutputRecord
from capsim.sim.logic import Run
from waffle import Flag


class BasicViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")
        Flag.objects.create(name='simulation', everyone=True)

    def test_runs(self):
        response = self.c.get("/run/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("<ul>" in response.content)

    def test_run(self):
        u = User.objects.create(username='test')
        rr = RunRecord.objects.create(user=u)
        r = Run(ticks=10, number_agents=10)
        rr.from_run(r)
        ror = RunOutputRecord.objects.create(run=rr)
        out = r.run()
        ror.from_runoutput(out)
        response = self.c.get("/run/%d/" % rr.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("<h2>Saved Run: " in response.content)

    def test_run_json(self):
        u = User.objects.create(username='test')
        rr = RunRecord.objects.create(user=u)
        r = Run(ticks=10, number_agents=10)
        rr.from_run(r)
        ror = RunOutputRecord.objects.create(run=rr)
        out = r.run()
        ror.from_runoutput(out)
        response = self.c.get("/run/%d/json/" % rr.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("agents_mass" in response.content)
