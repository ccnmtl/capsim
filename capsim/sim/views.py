from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View
from capsim.sim.models import RunRecord
from capsim.main.views import LoggedInMixin
from json import dumps, loads


class RunsView(LoggedInMixin, ListView):
    template_name = 'sim/runs.html'
    model = RunRecord
    context_object_name = 'runs'

    def get_queryset(self):
        return RunRecord.objects.filter(user=self.request.user)


class RunView(LoggedInMixin, TemplateView):
    template_name = 'sim/run.html'

    def get_context_data(self, id):
        rr = get_object_or_404(RunRecord, id=id)
        out = rr.runoutput().get_runoutput()
        d = out.display_data()
        d.update(run=rr)
        return d


class CompareRunsView(LoggedInMixin, TemplateView):
    template_name = "sim/compare_runs.html"

    def get_context_data(self):
        runs = []
        for k in self.request.GET.keys():
            if not k.startswith('run'):
                continue
            id = k.split('_')[1]

            rr = get_object_or_404(RunRecord, id=id)
            out = rr.runoutput().get_runoutput()
            d = out.display_data()
            d.update(run=rr)
            runs.append(d)
        return dict(runs=runs)


class RunEditView(LoggedInMixin, View):
    def post(self, request, pk):
        rr = get_object_or_404(RunRecord, pk=pk)
        rr.title = request.POST.get('title', '')
        rr.description = request.POST.get('description', '')
        rr.save()
        return HttpResponseRedirect(rr.get_absolute_url())


class RunOutputView(LoggedInMixin, View):
    def get(self, request, pk):
        rr = get_object_or_404(RunRecord, pk=pk)
        out = loads(rr.runoutput().data)
        return HttpResponse(
            dumps(out['data']),
            content_type="application/json")
