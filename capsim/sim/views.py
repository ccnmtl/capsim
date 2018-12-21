from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View

from capsim.sim.models import (
    RunRecord, Experiment, Intervention, InterventionLevel,
    Parameter, merge_parameters_into_form)

from capsim.main.views import LoggedInMixin
from capsim.main.forms import (
    RunForm, ExperimentForm, ALL_FIELDS, FLOAT_FIELDS)
from capsim.sim.tasks import (
    run_experiment, generate_full_csv, process_run)

import csv
from json import dumps, loads


class ParameterListView(LoggedInMixin, ListView):
    model = Parameter


class ParameterAddView(LoggedInMixin, View):
    template_name = "sim/parameter_add.html"
    model = Parameter

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        self.model.objects.create(
            slug=request.POST.get('slug', 'no-slug'),
            num_type=request.POST.get('num_type', 'float'),
            value=request.POST.get('value', '0.0'))
        return HttpResponseRedirect("/calibrate/parameter/")


class ParameterEditView(LoggedInMixin, View):
    template_name = "sim/parameter_edit.html"
    model = Parameter

    def get(self, request, pk):
        return render(
            request, self.template_name,
            dict(object=get_object_or_404(self.model, pk=pk)))

    def post(self, request, pk):
        parameter = get_object_or_404(self.model, pk=pk)
        parameter.num_type = request.POST.get('num_type', 'float')
        parameter.value = request.POST.get('value', '0.0')
        parameter.save()
        return HttpResponseRedirect(parameter.get_absolute_url())


class InterventionListView(LoggedInMixin, ListView):
    model = Intervention


class InterventionAddView(LoggedInMixin, View):
    template_name = "sim/intervention_add.html"
    model = Intervention

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        i = self.model.objects.create(
            name=request.POST.get('name', 'no name'),
            slug=request.POST.get('slug', 'no-slug'))
        InterventionLevel.objects.create(
            intervention=i,
            level="high",
            cost=request.POST.get('high_cost', '0'))
        InterventionLevel.objects.create(
            intervention=i,
            level="medium",
            cost=request.POST.get('medium_cost', '0'))
        InterventionLevel.objects.create(
            intervention=i,
            level="low",
            cost=request.POST.get('low_cost', '0'))
        return HttpResponseRedirect("/calibrate/intervention/")


class InterventionSetCostsView(LoggedInMixin, View):
    def post(self, request):
        for k in list(request.POST.keys()):
            (level, _, intervention_id) = k.split("_")
            cost = request.POST.get(k, "0")
            i = Intervention.objects.get(pk=intervention_id)
            il = i.interventionlevel_set.filter(level=level)[0]
            il.cost = cost
            il.save()
        return HttpResponseRedirect("/calibrate/intervention/")


class InterventionEditView(LoggedInMixin, View):
    template_name = "sim/intervention_edit.html"
    model = Intervention

    def get(self, request, pk):
        return render(
            request, self.template_name,
            dict(object=get_object_or_404(self.model, pk=pk),
                 parameters=FLOAT_FIELDS))

    def post(self, request, pk):
        intervention = get_object_or_404(self.model, pk=pk)
        intervention.clear_all_modifiers()
        for k in list(request.POST.keys()):
            (level, t, n) = k.split("_")
            if t != "parameter":
                continue
            parameter = request.POST[k]
            value = request.POST.get("%s_adjustment_%s" % (level, n), "0.0")
            if parameter == "" or value == "0.0" or value == "" or value == "":
                continue
            intervention.add_modifier(level, parameter, value)
        return HttpResponseRedirect(intervention.get_absolute_url())


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
        for k in list(self.request.GET.keys()):
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
        r = HttpResponse(content_type='application/json')
        r['Content-Disposition'] = (
            "attachment; filename=capsim_run_%d.json" % rr.id)
        r.write(dumps(loads(out['data'])))
        return r


class ExperimentOutputView(LoggedInMixin, View):
    def get(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename=capsim_experiment_%d.csv' % experiment.id)
        writer = csv.writer(response)
        headers = ['trial', experiment.independent_variable,
                   experiment.dependent_variable, 'mass']
        writer.writerow(headers)
        for er in experiment.exprun_set.all():
            writer.writerow(
                [er.trial, er.independent_value,
                 er.dependent_value, er.mass])
        return response


class ExperimentFullOutputView(LoggedInMixin, View):
    def get(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        generate_full_csv.delay(experiment_id=experiment.id)
        return HttpResponse(
            """CSV is being generated. After a few minutes it will be available
            <a href="%s">here</a>.""" % experiment.full_csv_url())


class ExperimentDeleteView(LoggedInMixin, View):
    template_name = "sim/experiment_delete.html"

    def get(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        return render(request, self.template_name,
                      dict(experiment=experiment))

    def post(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        experiment.delete_csv_file()
        for er in experiment.exprun_set.all():
            er.run.delete()
            er.delete()
        experiment.delete()
        return HttpResponseRedirect("/experiment/")


class ExperimentReEnqueueView(LoggedInMixin, View):
    def get(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        for er in experiment.exprun_set.filter(status='enqueued'):
            process_run.delay(er.run.id, er.id)
        return HttpResponseRedirect(experiment.get_absolute_url())


class NewExperimentView(LoggedInMixin, View):
    template_name = 'sim/new_experiment.html'

    @transaction.atomic()
    def post(self, request):
        sp1 = transaction.savepoint()
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

            total = int(independent_steps) * int(dependent_steps) * int(trials)
            experiment = Experiment.objects.create(
                user=request.user,
                title=title,
                status="enqueued",
                data=dumps(parameters),
                independent_variable=independent_variable,
                dependent_variable=dependent_variable,

                independent_min=independent_min,
                independent_max=independent_max,
                independent_steps=independent_steps,

                dependent_min=dependent_min,
                dependent_max=dependent_max,
                dependent_steps=dependent_steps,

                trials=trials,
                total=total,
                completed=0,
                )
            experiment.normalize_title()
            redirect_url = experiment.get_absolute_url()
            transaction.savepoint_commit(sp1)
            run_experiment.delay(experiment_id=experiment.id)
            return HttpResponseRedirect(redirect_url)
        transaction.savepoint_commit(sp1)
        parameters = Parameter.objects.all()
        form = merge_parameters_into_form(form, parameters)
        return render(request, self.template_name,
                      dict(form=form, expform=expform))

    def get(self, request):
        form = RunForm()
        parameters = Parameter.objects.all()
        form = merge_parameters_into_form(form, parameters)
        return render(request, self.template_name,
                      dict(form=form,
                           expform=ExperimentForm(),
                           ))
