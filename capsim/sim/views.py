from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View
from capsim.sim.models import RunRecord
from json import dumps, loads
import numpy as np


class RunsView(ListView):
    template_name = 'sim/runs.html'
    model = RunRecord
    context_object_name = 'runs'


class RunView(TemplateView):
    template_name = 'sim/run.html'

    def get_context_data(self, id):
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


class RunOutputView(View):
    def get(self, request, pk):
        rr = get_object_or_404(RunRecord, pk=pk)
        out = loads(rr.runoutput().data)
        return HttpResponse(
            dumps(out['data']),
            content_type="application/json")
