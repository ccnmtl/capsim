from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
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


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class PageView(View):
    hierarchy_name = "main"
    hierarchy_base = "/pages/"

    def hierarchy(self):
        return get_hierarchy(self.hierarchy_name, self.hierarchy_base)

    def get(self, request, path):
        return self.handler(request, path)

    def post(self, request, path):
        return self.handler(request, path)


class ViewPage(PageView):
    def handler(self, request, path):
        return generic_view_page(request, path, hierarchy=self.hierarchy())


class EditPage(LoggedInMixin, PageView):
    def handler(self, request, path):
        return generic_edit_page(request, path, hierarchy=self.hierarchy())


class InstructorPage(LoggedInMixin, PageView):
    def handler(self, request, path):
        return generic_instructor_page(request, path,
                                       hierarchy=self.hierarchy())
