from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from capsim.sim.logic import Run
from capsim.sim.models import RunRecord, RunOutputRecord


@render_to('main/index.html')
def index(request):
    if request.method == "POST":
        ticks = int(request.POST.get('ticks', 100))
        number_agents = int(request.POST.get('number_agents', 100))
        r = Run(ticks=ticks, number_agents=number_agents)
        rr = RunRecord()
        rr.from_run(r)
        out = r.run()
        ror = RunOutputRecord(run=rr)
        ror.from_runoutput(out)
        return HttpResponseRedirect(rr.get_absolute_url())
    else:
        return dict(number_agents=100, ticks=100)
