from django.test import TestCase
from django.test.client import Client
from pagetree.helpers import get_hierarchy
from django.contrib.auth.models import User

from waffle.models import Flag


class BasicViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username='testuser')
        self.u.set_password('test')
        self.u.save()
        self.c.login(username="testuser", password="test")
        Flag.objects.create(name='simulation', everyone=True)

    def test_root(self):
        response = self.c.get("/run/new/")
        self.assertEquals(response.status_code, 200)

    def test_root_post_invalid(self):
        response = self.c.post("/run/new/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("errorlist" in response.content)

    def test_root_post_valid(self):
        response = self.c.post(
            "/run/new/",
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
                 ))
        self.assertEquals(response.status_code, 302)

    def test_demo_mode(self):
        Flag.objects.create(name='demo_mode', everyone=True)
        response = self.c.post(
            "/run/new/",
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
                 intervention_increase_physical_activity='high',
                 ))
        self.assertEquals(response.status_code, 302)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class PagetreeViewTestsLoggedOut(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })

    def test_page(self):
        r = self.c.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_page_post(self):
        r = self.c.post("/pages/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_edit_page(self):
        r = self.c.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.c.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedIn(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_page(self):
        r = self.c.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_page(self):
        r = self.c.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 200)
