from django.test import TestCase
from capsim.sim.models import RunRecord, RunOutputRecord
from capsim.sim.logic import Run


class RunRecordTest(TestCase):
    def test_serialization(self):
        rr = RunRecord.objects.create()
        run = Run(ticks=100)
        rr.from_run(run)
        run2 = rr.get_run()
        self.assertEqual(run.ticks, run2.ticks)


class RunOutputRecordTest(TestCase):
    def test_serialization(self):
        rr = RunRecord.objects.create()
        r = Run(ticks=100)
        rr.from_run(r)
        out = r.run()
        ror = RunOutputRecord.objects.create(run=rr)
        ror.from_runoutput(out)
        out2 = ror.get_runoutput()
        self.assertEqual(out.ticks, out2.ticks)
