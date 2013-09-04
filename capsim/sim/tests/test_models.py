from django.test import TestCase
from capsim.sim.models import RunRecord
from capsim.sim.logic import Run


class RunRecordTest(TestCase):
    def test_serialization(self):
        rr = RunRecord.objects.create()
        run = Run(ticks=100)
        rr.from_run(run)
        run2 = rr.get_run()
        self.assertEqual(run.ticks, run2.ticks)
