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
        self.flag = Flag.objects.create(name='simulation', everyone=True)

    def test_run_form(self):
        response = self.c.get("/run/new/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("id=\"test-new-run-form\"" in response.content)

    def test_run_form_disabled(self):
        self.flag.everyone = False
        self.flag.save()
        response = self.c.get("/run/new/")
        self.assertEquals(response.status_code, 200)
        self.assertFalse("id=\"test-new-run-form\"" in response.content)

    def test_runs(self):
        response = self.c.get("/run/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("<p>No saved runs yet.</p>" in response.content)

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

    def test_edit_run(self):
        u = User.objects.create(username='test')
        rr = RunRecord.objects.create(user=u)

        response = self.c.post(
            "/run/%d/edit/" % rr.id,
            dict(title="test title", description="test description"))
        self.assertEquals(response.status_code, 302)
        rr2 = RunRecord.objects.get(id=rr.id)
        self.assertEquals(rr2.title, "test title")
        self.assertEquals(rr2.description, "test description")

    def test_compare_runs_empty(self):
        response = self.c.get("/run/compare/")
        self.assertEquals(response.status_code, 200)

    def test_compare_runs_bad_param(self):
        response = self.c.get("/run/compare/?someparam=whatever")
        self.assertEquals(response.status_code, 200)

    def test_compare_runs(self):
        u = User.objects.create(username='test')
        rr = RunRecord.objects.create(user=u)
        r = Run(ticks=10, number_agents=10)
        rr.from_run(r)
        ror = RunOutputRecord.objects.create(run=rr)
        out = r.run()
        ror.from_runoutput(out)
        response = self.c.get("/run/compare/?run_%d=on" % rr.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("makeGraph" in response.content)

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
