from annoying.decorators import render_to
from capsim.sim.logic import Simulation
from django.http import HttpResponse
from datetime import datetime


@render_to('main/index.html')
def index(request):
    if request.method == "POST":
        ticks = int(request.POST.get('ticks', 100))
        number_agents = int(request.POST.get('number_agents', 100))
        start = datetime.now()
        s = Simulation(number_agents=number_agents)
        for t in range(ticks):
            s.tick()
        end = datetime.now()
        elapsed = (end - start).microseconds / 1000.
        return dict(number_agents=number_agents, ticks=ticks, time=elapsed, ran=True)
    else:
        return dict()
