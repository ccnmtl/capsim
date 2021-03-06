import capsim.main.views
from capsim.sim.models import RunRecord, Experiment, Parameter
import capsim.sim.views
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
import django.views.static
from infranil.views import InfranilView
from pagetree.generic.views import PageView


admin.autodiscover()

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))
if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))

urlpatterns = [
    auth_urls,
    url(r'^$', TemplateView.as_view(template_name="main/home.html")),
    path('accounts/profile/', RedirectView.as_view(url='/'),
         name='go-to-homepage'),
    url(r'^contact/$', TemplateView.as_view(
        template_name="main/contact.html")),
    url(r'^about/$', TemplateView.as_view(template_name="main/about.html")),
    url(r'^topics/$', TemplateView.as_view(template_name="main/topics.html")),
    url(r'^topic-obesity/$', TemplateView.as_view(
        template_name="sim/topic-obesity.html")),
    url(r'^topic-obesity-debrief/$', TemplateView.as_view(
        template_name="sim/topic-obesity-debrief.html")),
    url(r'^proposal/$', TemplateView.as_view(
        template_name="sim/proposal.html")),
    url(r'^run/new/$', capsim.main.views.NewRunView.as_view()),
    url(r'^run/$', capsim.sim.views.RunsView.as_view()),
    url(r'^run/compare/$', capsim.sim.views.CompareRunsView.as_view()),
    url(r'^run/toggle/$', capsim.main.views.ToggleFlagView.as_view()),
    url(r'^run/(?P<id>\d+)/$', capsim.sim.views.RunView.as_view()),
    url(r'^run/(?P<pk>\d+)/json/$', capsim.sim.views.RunOutputView.as_view()),
    url(r'^run/(?P<pk>\d+)/edit/$', capsim.sim.views.RunEditView.as_view()),
    url(r'^run/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(model=RunRecord, success_url="/run/")),

    url(r'^experiment/new/$', capsim.sim.views.NewExperimentView.as_view()),
    url(r'^experiment/$', capsim.sim.views.ExperimentListView.as_view()),
    url(r'^experiment/(?P<pk>\d+)/$', DetailView.as_view(model=Experiment)),
    url(r'^experiment/(?P<pk>\d+)/csv/$',
        capsim.sim.views.ExperimentOutputView.as_view()),
    url(r'^experiment/(?P<pk>\d+)/fullcsv/$',
        capsim.sim.views.ExperimentFullOutputView.as_view()),
    url(r'^experiment/(?P<pk>\d+)/heatmap/$',
        DetailView.as_view(
            model=Experiment,
            template_name="sim/experiment_heatmap.html")),
    url(r'^experiment/(?P<pk>\d+)/delete/$',
        capsim.sim.views.ExperimentDeleteView.as_view()),
    url(r'^experiment/(?P<pk>\d+)/reenqueue/$',
        capsim.sim.views.ExperimentReEnqueueView.as_view()),

    url(r'^calibrate/$', TemplateView.as_view(
        template_name="sim/calibrate_index.html")),
    url(r'^calibrate/intervention/$',
        capsim.sim.views.InterventionListView.as_view()),
    url(r'^calibrate/intervention/(?P<pk>\d+)/$',
        capsim.sim.views.InterventionEditView.as_view()),
    url(r'^calibrate/intervention/add/$',
        capsim.sim.views.InterventionAddView.as_view()),
    url(r'^calibrate/intervention/set_costs/$',
        capsim.sim.views.InterventionSetCostsView.as_view()),

    url(r'^calibrate/parameter/$',
        capsim.sim.views.ParameterListView.as_view()),
    url(r'^calibrate/parameter/(?P<pk>\d+)/$',
        capsim.sim.views.ParameterEditView.as_view()),
    url(r'^calibrate/parameter/add/$',
        capsim.sim.views.ParameterAddView.as_view()),
    url(r'^calibrate/parameter/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(
            model=Parameter,
            success_url="/calibrate/parameter/")),

    url(r'^admin/', admin.site.urls),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/', TemplateView.as_view(template_name="stats.html")),
    url(r'^model/', TemplateView.as_view(template_name="main/model.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^infranil/(?P<path>.*)$', InfranilView.as_view()),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^quizblock/', include('quizblock.urls')),
    url(r'^pages/edit/(?P<path>.*)$', capsim.main.views.EditPage.as_view(),
        {}, 'edit-page'),
    url(r'^pages/instructor/(?P<path>.*)$',
        capsim.main.views.InstructorPage.as_view()),
    url(r'^pages/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
