from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from pagetree.generic.views import EditView
from pagetree.generic.views import InstructorView
from capsim.sim.logic import Run
from capsim.sim.models import (
    RunRecord, RunOutputRecord, Intervention, Parameter,
    merge_parameters_into_form)
from waffle import Flag
import waffle
from .forms import RunForm, ALL_FIELDS


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


def apply_skews(request, skew_params):
    i_s = settings.INTERVENTION_SKEWS
    for k in request.POST.keys():
        if not k.startswith('intervention_'):
            continue
        v = request.POST[k]
        if (k, v) in i_s:
            for f in ['mass', 'intake', 'expenditure']:
                skew_params[f] += i_s[(k, v)].get(f, 0.)
    return skew_params


def template_safe(k):
    """ convert slugs into ones that we can use as attributes
    in the template. Ie,

    {{by_slug.increase-physical-activity}}

    would be a syntax error, but

    {{by_slug.increase_physical_activity}}

    is ok."""
    return k.replace('-', '_')


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
            skew_params = dict(mass=0., intake=0., expenditure=0.)

            if waffle.flag_is_active(request, 'demo_mode'):
                skew_params = apply_skews(request, skew_params)
            ror.from_runoutput(out, skew_params)
            return HttpResponseRedirect(rr.get_absolute_url())
        return render(
            request, self.template_name,
            dict(form=form, interventions=Intervention.objects.all(),
                 parameters=Parameter.objects.all()))

    def get(self, request):
        form = RunForm()
        parameters = Parameter.objects.all()
        form = merge_parameters_into_form(form, parameters)
        by_slug = {template_safe(i.slug): i
                   for i in Intervention.objects.all()}
        return render(
            request, self.template_name,
            dict(form=form, interventions=Intervention.objects.all(),
                 by_slug=by_slug,
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
