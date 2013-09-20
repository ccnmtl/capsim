from annoying.decorators import render_to
from capsim.sim.models import RunRecord


@render_to('main/runs.html')
def runs(request):
    return dict(runs=RunRecord.objects.all())
