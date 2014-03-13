from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View

from capsim.sim.models import RunRecord, Experiment
from capsim.main.views import LoggedInMixin
from capsim.main.forms import RunForm, ExperimentForm, ALL_FIELDS

from json import dumps, loads


class RunsView(LoggedInMixin, ListView):
    template_name = 'sim/runs.html'
    model = RunRecord
    context_object_name = 'runs'

    def get_queryset(self):
        return RunRecord.objects.filter(user=self.request.user)


class ExperimentListView(LoggedInMixin, ListView):
    model = Experiment

    def get_queryset(self):
        return Experiment.objects.filter(user=self.request.user)


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


class NewExperimentView(LoggedInMixin, View):
    template_name = 'sim/new_experiment.html'

    def post(self, request):
        form = RunForm(request.POST)
        expform = ExperimentForm(request.POST)
        if form.is_valid() and expform.is_valid():
            parameters = dict()
            for f in ALL_FIELDS:
                parameters[f] = form.cleaned_data[f]

            title = expform.cleaned_data['title']
            trials = expform.cleaned_data['trials']
            independent_variable = expform.cleaned_data['independent_variable']
            dependent_variable = expform.cleaned_data['dependent_variable']

            independent_min = expform.cleaned_data['independent_min']
            independent_max = expform.cleaned_data['independent_max']
            independent_steps = expform.cleaned_data['independent_steps']

            dependent_min = expform.cleaned_data['dependent_min']
            dependent_max = expform.cleaned_data['dependent_max']
            dependent_steps = expform.cleaned_data['dependent_steps']

            experiment = Experiment.objects.create(
                user=request.user,
                title=title,
                status="enqueued",
                data=parameters,  # JSON
                independent_variable=independent_variable,
                dependent_variable=dependent_variable,

                independent_min=independent_min,
                independent_max=independent_max,
                independent_steps=independent_steps,

                dependent_min=dependent_min,
                dependent_max=dependent_max,
                dependent_steps=dependent_steps,

                trials=trials,
                total=1,
                completed=0,
                )
            return HttpResponseRedirect(experiment.get_absolute_url())
        return render(request, self.template_name,
                      dict(form=form, expform=expform))

    def get(self, request):
        return render(request, self.template_name,
                      dict(form=RunForm(),
                           expform=ExperimentForm(),
                           ))
