from annoying.decorators import render_to
from capsim.sim.logic import Run
from capsim.sim.models import RunRecord, RunOutputRecord
from datetime import datetime


@render_to('main/index.html')
def index(request):
    if request.method == "POST":
        ticks = int(request.POST.get('ticks', 100))
        number_agents = int(request.POST.get('number_agents', 100))
        start = datetime.now()
        r = Run(ticks=ticks, number_agents=number_agents)
        rr = RunRecord()
        rr.from_run(r)
        out = r.run()
        ror = RunOutputRecord(run=rr)
        ror.from_runoutput(out)
        output = out.data
        stats = [dict(mean=d.mean(), std=d.std()) for d in output.agents_mass]
        end = datetime.now()
        elapsed = (end - start).total_seconds()
        return dict(number_agents=number_agents, ticks=ticks, time=elapsed,
                    output=output,
                    stats=stats,
                    mean=output.agents_mass[ticks-1].mean(),
                    stddev=output.agents_mass[ticks-1].std(), ran=True)
    else:
        return dict(number_agents=100, ticks=100)


@render_to('main/runs.html')
def runs(request):
    return dict(runs=RunRecord.objects.all())
