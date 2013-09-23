from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from capsim.sim.models import RunRecord
import numpy as np


@render_to('sim/runs.html')
def runs(request):
    return dict(runs=RunRecord.objects.all())


@render_to('sim/run.html')
def run(request, id):
    rr = get_object_or_404(RunRecord, id=id)
    out = rr.runoutput().get_runoutput()
    ticks = out.ticks
    number_agents = out.params.get('number_agents', 100)
    output = out.data
    stats = [dict(mean=np.array(d).mean(), std=np.array(d).std())
             for d in output.agents_mass]
    return dict(number_agents=number_agents, ticks=ticks,
                output=output,
                stats=stats,
                mean=np.array(output.agents_mass[ticks-1]).mean(),
                stddev=np.array(output.agents_mass[ticks-1]).std(), run=rr)
