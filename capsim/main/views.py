from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from pagetree.generic.views import EditView
from pagetree.generic.views import InstructorView
from capsim.sim.logic import Run
from capsim.sim.models import RunRecord, RunOutputRecord
from .forms import RunForm


class IndexView(View):
    template_name = 'main/index.html'

    def post(self, request):
        form = RunForm(request.POST)
        if form.is_valid():
            fields = ['ticks', 'number_agents', 'gamma_1', 'gamma_2',
                      'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6',
                      'sigma_1', 'sigma_2']
            parameters = dict()
            for f in fields:
                parameters[f] = form.cleaned_data[f]
            r = Run(**parameters)
            rr = RunRecord()
            rr.from_run(r)
            out = r.run()
            ror = RunOutputRecord(run=rr)
            ror.from_runoutput(out)
            return HttpResponseRedirect(rr.get_absolute_url())
        return render(request, self.template_name, dict(form=form))

    def get(self, request):
        return render(request, self.template_name, dict(form=RunForm()))


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class EditPage(LoggedInMixin, EditView):
    hierarchy_name = "main"
    hierarchy_base = "/pages/"


class InstructorPage(LoggedInMixin, InstructorView):
    hierarchy_name = "main"
    hierarchy_base = "/pages/"
