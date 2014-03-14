from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from capsim.sim.models import RunRecord, RunOutputRecord
from capsim.sim.logic import Run
from waffle import Flag
from .factories import ExpRunFactory


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

    def test_toggle_flag(self):
        response = self.c.post("/run/toggle/", dict())
        self.assertEquals(response.status_code, 302)
        f = Flag.objects.get(name='simulation')
        self.assertFalse(f.everyone == self.flag.everyone)

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


class ExperimentViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")
        self.flag = Flag.objects.create(name='simulation', everyone=True)

    def test_experiment_list(self):
        response = self.c.get("/experiment/")
        self.assertEquals(response.status_code, 200)

    def test_experiment_form(self):
        response = self.c.get("/experiment/new/")
        self.assertEquals(response.status_code, 200)

    def test_experiment_post_invalid(self):
        response = self.c.post("/experiment/new/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("errorlist" in response.content)

    def test_experiment_post_valid(self):
        response = self.c.post(
            "/experiment/new/",
            dict(ticks=10, number_agents=10,
                 gamma_1=1.0, gamma_2=1.0, gamma_3=1.0, gamma_4=1.0,
                 gamma_5=1.0, gamma_6=1.0,
                 sigma_1=6.2, sigma_2=5.,
                 agent_initial_mass_mean=100., agent_initial_mass_sigma=20.,
                 agent_base_output_mean=100., agent_base_output_sigma=5.,
                 recreation_activity_alpha=0.5, recreation_activity_lambda=0.1,
                 domestic_activity_alpha=0.5, domestic_activity_lambda=0.1,
                 transport_activity_alpha=0.5, transport_activity_lambda=0.1,
                 education_activity_alpha=0.5, education_activity_lambda=0.1,
                 food_exposure_alpha=0.5, food_exposure_lambda=0.1,
                 energy_density_alpha=0.5, energy_density_lambda=0.1,
                 food_advertising_alpha=0.5, food_advertising_lambda=0.1,
                 food_convenience_alpha=0.5, food_convenience_lambda=0.1,
                 food_literacy_alpha=0.5, food_literacy_lambda=0.1,

                 recreation_activity_weight=1.0,
                 domestic_activity_weight=1.0,
                 transport_activity_weight=1.0,
                 education_activity_weight=1.0,

                 food_exposure_weight=1.0,
                 energy_density_weight=1.0,
                 food_advertising_weight=1.0,
                 food_convenience_weight=1.0,
                 food_literacy_weight=1.0,

                 title="new experiment",
                 independent_variable="gamma_1",
                 dependent_variable="gamma_2",

                 independent_min=0.0,
                 independent_max=1.0,
                 independent_steps=1,

                 dependent_min=0.0,
                 dependent_max=1.0,
                 dependent_steps=1,

                 trials=1,
                 ))
        self.assertEquals(response.status_code, 302)

    def test_csv(self):
        er = ExpRunFactory()
        r = self.c.get(er.experiment.get_absolute_url() + "csv/")
        self.assertEqual(r.status_code, 200)
