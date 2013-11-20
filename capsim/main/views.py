from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from pagetree.helpers import get_hierarchy
from pagetree.generic.views import generic_view_page
from pagetree.generic.views import generic_edit_page
from pagetree.generic.views import generic_instructor_page
from capsim.sim.logic import Run
from capsim.sim.models import RunRecord, RunOutputRecord
from .forms import RunForm


class IndexView(View):
    template_name = 'main/index.html'

    def post(self, request):
        form = RunForm(request.POST)
        if form.is_valid():
            ticks = form.cleaned_data['ticks']
            number_agents = form.cleaned_data['number_agents']
            r = Run(ticks=ticks, number_agents=number_agents)
            rr = RunRecord()
            rr.from_run(r)
            out = r.run()
            ror = RunOutputRecord(run=rr)
            ror.from_runoutput(out)
            return HttpResponseRedirect(rr.get_absolute_url())
        return render(request, self.template_name, dict(form=form))

    def get(self, request):
        return render(request, self.template_name, dict(form=RunForm()))


def page(request, path):
    # do auth on the request if you need the user to be logged in
    # or only want some particular users to be able to get here
    h = get_hierarchy("main", "/pages/")
    return generic_view_page(request, path, hierarchy=h)


@login_required
def edit_page(request, path):
    # do any additional auth here
    h = get_hierarchy("main", "/pages/")
    return generic_edit_page(request, path, hierarchy=h)


@login_required
def instructor_page(request, path):
    # do any additional auth here
    h = get_hierarchy("main", "/pages/")
    return generic_instructor_page(request, path, hierarchy=h)
