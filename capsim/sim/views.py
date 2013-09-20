from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from capsim.sim.models import RunRecord


@render_to('sim/runs.html')
def runs(request):
    return dict(runs=RunRecord.objects.all())


@render_to('sim/run.html')
def run(request, id):
    r = get_object_or_404(RunRecord, id=id)
    return dict(run=r)
