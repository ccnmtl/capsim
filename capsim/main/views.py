from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from pagetree.generic.views import EditView
from pagetree.generic.views import InstructorView
from capsim.sim.logic import Run
from capsim.sim.models import (
    RunRecord, RunOutputRecord, Intervention, Parameter,
    merge_parameters_into_form)
from waffle import Flag
from .forms import RunForm, ALL_FIELDS


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class NewRunView(LoggedInMixin, View):
    template_name = 'main/index.html'

    def post(self, request):
        form = RunForm(request.POST)
        if form.is_valid():
            parameters = dict()
            for f in ALL_FIELDS:
                parameters[f] = form.cleaned_data[f]
            r = Run(**parameters)
            rr = RunRecord()
            rr.user = request.user
            rr.from_run(r)
            out = r.run()
            ror = RunOutputRecord(run=rr)
            ror.from_runoutput(out)
            return HttpResponseRedirect(rr.get_absolute_url())
        return render(
            request, self.template_name,
            dict(form=form, interventions=Intervention.objects.all(),
                 parameters=Parameter.objects.all()))

    def get(self, request):
        form = RunForm()
        parameters = Parameter.objects.all()
        form = merge_parameters_into_form(form, parameters)
        return render(
            request, self.template_name,
            dict(form=form, interventions=Intervention.objects.all(),
                 parameters=parameters))


class ToggleFlagView(LoggedInMixin, View):
    def post(self, request):
        flag, _ = Flag.objects.get_or_create(name='simulation',
                                             defaults={'everyone': False})
        flag.everyone = not flag.everyone
        flag.save()
        return HttpResponseRedirect("/run/new/")


class EditPage(LoggedInMixin, EditView):
    hierarchy_name = "main"
    hierarchy_base = "/pages/"


class InstructorPage(LoggedInMixin, InstructorView):
    hierarchy_name = "main"
    hierarchy_base = "/pages/"
