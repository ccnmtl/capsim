from django.contrib.auth.models import User
from django.test import TestCase
from capsim.sim.models import RunRecord, RunOutputRecord
from capsim.sim.logic import Run
from .factories import ExperimentFactory, ExpRunFactory


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
