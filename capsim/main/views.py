from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from pagetree.generic.views import EditView
from pagetree.generic.views import InstructorView
from capsim.sim.logic import Run
from capsim.sim.models import RunRecord, RunOutputRecord
from waffle import Flag
from .forms import RunForm


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class NewRunView(LoggedInMixin, View):
    template_name = 'main/index.html'

    def post(self, request):
        form = RunForm(request.POST)
        if form.is_valid():
            fields = ['ticks', 'number_agents', 'gamma_1', 'gamma_2',
                      'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6',
                      'sigma_1', 'sigma_2',
                      'agent_initial_mass_mean', 'agent_initial_mass_sigma',
                      'agent_base_output_mean', 'agent_base_output_sigma',
                      'recreation_activity_alpha',
                      'recreation_activity_lambda',
                      'domestic_activity_alpha',
                      'domestic_activity_lambda',
                      'transport_activity_alpha',
                      'transport_activity_lambda',
                      'education_activity_alpha',
                      'education_activity_lambda',
                      'food_exposure_alpha',
                      'food_exposure_lambda',
                      'energy_density_alpha',
                      'energy_density_lambda',
                      'food_advertising_alpha',
                      'food_advertising_lambda',
                      'food_convenience_alpha',
                      'food_convenience_lambda',
                      'food_literacy_alpha',
                      'food_literacy_lambda',
                      ]
            parameters = dict()
            for f in fields:
                parameters[f] = form.cleaned_data[f]
            r = Run(**parameters)
            rr = RunRecord()
            rr.user = request.user
            rr.from_run(r)
            out = r.run()
            ror = RunOutputRecord(run=rr)
            ror.from_runoutput(out)
            return HttpResponseRedirect(rr.get_absolute_url())
        return render(request, self.template_name, dict(form=form))

    def get(self, request):
        return render(request, self.template_name, dict(form=RunForm()))


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
