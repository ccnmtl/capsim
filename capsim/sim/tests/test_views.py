from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from capsim.sim.models import (
    RunRecord, RunOutputRecord, Intervention, Parameter
)
from capsim.sim.logic import Run
from waffle.models import Flag

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
        self.assertContains(response, "id=\"test-new-run-form\"")

    def test_run_form_disabled(self):
        self.flag.everyone = False
        self.flag.save()
        response = self.c.get("/run/new/")
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, "id=\"test-new-run-form\"")

    def test_toggle_flag(self):
        response = self.c.post("/run/toggle/", dict())
        self.assertEquals(response.status_code, 302)
        f = Flag.objects.get(name='simulation')
        self.assertFalse(f.everyone == self.flag.everyone)

    def test_runs(self):
        response = self.c.get("/run/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<p>No saved runs yet.</p>")

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
        self.assertContains(response, "<h2>Saved Run: ")

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
        self.assertContains(response, "makeGraph")

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
        self.assertContains(response, "agents_mass")


class ExperimentViewTest(TestCase):
    def setUp(self):
        super().setUp()
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
        self.assertContains(response, "errorlist")

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

    def test_delete_experimeent(self):
        er = ExpRunFactory()
        r = self.c.get(er.experiment.get_absolute_url() + "delete/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "<form")
        r = self.c.post(er.experiment.get_absolute_url() + "delete/")
        self.assertEqual(r.status_code, 302)


class InterventionViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")
        self.flag = Flag.objects.create(name='simulation', everyone=True)

    def test_runthrough(self):
        """ a quick end-to-end run through for now. replace with
        more granular unit tests later"""
        response = self.c.get("/calibrate/intervention/add/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<form")

        response = self.c.post(
            "/calibrate/intervention/add/",
            dict(
                name="new intervention", slug="new-intervention",
                high_cost="300", medium_cost="200", low_cost="100"))
        self.assertEquals(response.status_code, 302)

        response = self.c.get("/calibrate/intervention/")
        self.assertContains(response, "new intervention")

        i = Intervention.objects.all()[0]
        response = self.c.post(
            "/calibrate/intervention/set_costs/",
            {
                "high_cost_%d" % i.id: "400",
                "medium_cost_%d" % i.id: "200",
                "low_cost_%d" % i.id: "100",
            })
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/calibrate/intervention/")
        self.assertContains(response, "400")

        response = self.c.get(i.get_absolute_url())
        self.assertEquals(response.status_code, 200)

        response = self.c.post(
            i.get_absolute_url(),
            dict(high_parameter_0="gamma_1",
                 high_adjustment_0="1.0",
                 medium_parameter_0="gamma_1",
                 medium_adjustment_0="0.0"))


class ParameterViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")
        self.flag = Flag.objects.create(name='simulation', everyone=True)

    def test_runthrough(self):
        """ a quick end-to-end run through for now. replace with
        more granular unit tests later"""
        response = self.c.get("/calibrate/parameter/add/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<form")

        response = self.c.post(
            "/calibrate/parameter/add/",
            dict(slug="new_parameter",
                 num_type="float", value="1.0"))
        self.assertEquals(response.status_code, 302)

        response = self.c.get("/calibrate/parameter/")
        self.assertContains(response, "new_parameter")

        p = Parameter.objects.all()[0]
        response = self.c.post(
            "/calibrate/parameter/%d/" % p.id,
            dict(num_type="float",
                 value="2.0",
                 ))
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/calibrate/parameter/")
        self.assertContains(response, "2.0")

        response = self.c.get(p.get_absolute_url())
        self.assertEquals(response.status_code, 200)
