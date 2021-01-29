from django.contrib.auth.models import User
from django.test import TestCase
from capsim.sim.models import (
    RunRecord, RunOutputRecord, merge_parameters_into_form,
    Parameter)
from capsim.sim.logic import Run
from .factories import (
    ExperimentFactory, ExpRunFactory, InterventionLevelFactory,
    ParameterFactory)


class RunRecordTest(TestCase):
    def test_serialization(self):
        u = User.objects.create(username='test')
        rr = RunRecord.objects.create(user=u)
        run = Run(ticks=100)
        rr.from_run(run)
        run2 = rr.get_run()
        self.assertEqual(run.ticks, run2.ticks)


class RunOutputRecordTest(TestCase):
    def test_serialization(self):
        u = User.objects.create(username='test')
        rr = RunRecord.objects.create(user=u)
        r = Run(ticks=100)
        rr.from_run(r)
        out = r.run()
        ror = RunOutputRecord.objects.create(run=rr)
        ror.from_runoutput(out)
        out2 = ror.get_runoutput()
        self.assertEqual(out.ticks, out2.ticks)


class ExperimentTest(TestCase):
    def test_populate(self):
        e = ExperimentFactory(trials=1,
                              independent_min=0.0,
                              independent_max=1.0,
                              independent_steps=1,
                              dependent_min=0.0,
                              dependent_max=1.0,
                              dependent_steps=1)
        e.populate(callback=None)
        self.assertEqual(e.status, "processing")

    def test_check_if_complete(self):
        er = ExpRunFactory()
        e = er.experiment
        e.total = 1
        e.save()
        e.check_if_complete()
        self.assertEqual(e.status, "enqueued")
        er.status = "complete"
        er.save()
        e.check_if_complete()
        self.assertEqual(e.status, "complete")

    def test_normalize_title(self):
        e = ExperimentFactory()
        e.title = ""
        e.save()
        e.normalize_title()
        self.assertTrue(e.title != "")
        e.normalize_title()
        self.assertTrue(e.title != "")

    def test_failed(self):
        er = ExpRunFactory()
        e = er.experiment
        er.failed()
        self.assertEqual(er.status, "failed")
        self.assertEqual(e.status, "failed")

    def test_full_csv_filename(self):
        er = ExpRunFactory()
        e = er.experiment
        self.assertTrue(e.full_csv_filename().startswith('experiment'))
        self.assertTrue(e.full_csv_filename().endswith('.csv'))

    def test_full_csv_url(self):
        er = ExpRunFactory()
        e = er.experiment
        self.assertTrue(e.full_csv_url().endswith('.csv'))

    def test_empty_heatmap(self):
        er = ExpRunFactory()
        e = er.experiment
        heatmap = e.heatmap()
        self.assertFalse(heatmap['data'])


class TestIntervention(TestCase):
    def test_add_modifier(self):
        il = InterventionLevelFactory()
        i = il.intervention
        i.add_modifier("medium", "foo", 1.0)
        self.assertEqual(i.interventionlevel_set.count(), 1)
        self.assertEqual(i.medium_modifiers().count(), 1)
        i.clear_all_modifiers()
        self.assertEqual(i.medium_modifiers().count(), 0)


class TestParameter(TestCase):
    def test_cast_value(self):
        p = ParameterFactory(num_type='int', value=0.0)
        self.assertEqual(p.cast_value(), 0)
        p = ParameterFactory(num_type='float', value=1.0)
        self.assertEqual(p.cast_value(), 1.0)


class TestMergeParameters(TestCase):
    def test_merge(self):
        ParameterFactory(slug="gamma_1", value="2.0")
        ParameterFactory(slug="gamma_2", value="2.0")

        class DummyField(object):
            initial = 1.0

        class DummyForm(object):
            fields = dict()

        f = DummyForm()
        f.fields['gamma_1'] = DummyField()

        new_form = merge_parameters_into_form(f, Parameter.objects.all())
        self.assertEqual(new_form.fields['gamma_1'].initial, 2.0)
