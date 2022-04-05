from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
import django.views.static
from infranil.views import InfranilView
from pagetree.generic.views import PageView

import capsim.main.views
from capsim.sim.models import RunRecord, Experiment, Parameter
import capsim.sim.views
from django_cas_ng import views as cas_views


admin.autodiscover()

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name="main/home.html")),
    path('accounts/profile/', RedirectView.as_view(url='/'),
         name='go-to-homepage'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    re_path(r'^contact/$', TemplateView.as_view(
        template_name="main/contact.html")),
    re_path(r'^about/$', TemplateView.as_view(template_name="main/about.html")),
    re_path(r'^topics/$', TemplateView.as_view(template_name="main/topics.html")),
    re_path(r'^topic-obesity/$', TemplateView.as_view(
        template_name="sim/topic-obesity.html")),
    re_path(r'^topic-obesity-debrief/$', TemplateView.as_view(
        template_name="sim/topic-obesity-debrief.html")),
    re_path(r'^proposal/$', TemplateView.as_view(
        template_name="sim/proposal.html")),
    re_path(r'^run/new/$', capsim.main.views.NewRunView.as_view()),
    re_path(r'^run/$', capsim.sim.views.RunsView.as_view()),
    re_path(r'^run/compare/$', capsim.sim.views.CompareRunsView.as_view()),
    re_path(r'^run/toggle/$', capsim.main.views.ToggleFlagView.as_view()),
    re_path(r'^run/(?P<id>\d+)/$', capsim.sim.views.RunView.as_view()),
    re_path(r'^run/(?P<pk>\d+)/json/$', capsim.sim.views.RunOutputView.as_view()),
    re_path(r'^run/(?P<pk>\d+)/edit/$', capsim.sim.views.RunEditView.as_view()),
    re_path(r'^run/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(model=RunRecord, success_url="/run/")),

    re_path(r'^experiment/new/$', capsim.sim.views.NewExperimentView.as_view()),
    re_path(r'^experiment/$', capsim.sim.views.ExperimentListView.as_view()),
    re_path(r'^experiment/(?P<pk>\d+)/$', DetailView.as_view(model=Experiment)),
    re_path(r'^experiment/(?P<pk>\d+)/csv/$',
        capsim.sim.views.ExperimentOutputView.as_view()),
    re_path(r'^experiment/(?P<pk>\d+)/fullcsv/$',
        capsim.sim.views.ExperimentFullOutputView.as_view()),
    re_path(r'^experiment/(?P<pk>\d+)/heatmap/$',
        DetailView.as_view(
            model=Experiment,
            template_name="sim/experiment_heatmap.html")),
    re_path(r'^experiment/(?P<pk>\d+)/delete/$',
        capsim.sim.views.ExperimentDeleteView.as_view()),
    re_path(r'^experiment/(?P<pk>\d+)/reenqueue/$',
        capsim.sim.views.ExperimentReEnqueueView.as_view()),

    re_path(r'^calibrate/$', TemplateView.as_view(
        template_name="sim/calibrate_index.html")),
    re_path(r'^calibrate/intervention/$',
        capsim.sim.views.InterventionListView.as_view()),
    re_path(r'^calibrate/intervention/(?P<pk>\d+)/$',
        capsim.sim.views.InterventionEditView.as_view()),
    re_path(r'^calibrate/intervention/add/$',
        capsim.sim.views.InterventionAddView.as_view()),
    re_path(r'^calibrate/intervention/set_costs/$',
        capsim.sim.views.InterventionSetCostsView.as_view()),

    re_path(r'^calibrate/parameter/$',
        capsim.sim.views.ParameterListView.as_view()),
    re_path(r'^calibrate/parameter/(?P<pk>\d+)/$',
        capsim.sim.views.ParameterEditView.as_view()),
    re_path(r'^calibrate/parameter/add/$',
        capsim.sim.views.ParameterAddView.as_view()),
    re_path(r'^calibrate/parameter/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(
            model=Parameter,
            success_url="/calibrate/parameter/")),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^_impersonate/', include('impersonate.urls')),
    re_path(r'^stats/', TemplateView.as_view(template_name="stats.html")),
    re_path(r'^model/', TemplateView.as_view(template_name="main/model.html")),
    re_path(r'smoketest/', include('smoketest.urls')),
    re_path(r'^infranil/(?P<path>.*)$', InfranilView.as_view()),
    re_path(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^pagetree/', include('pagetree.urls')),
    re_path(r'^quizblock/', include('quizblock.urls')),
    re_path(r'^pages/edit/(?P<path>.*)$', capsim.main.views.EditPage.as_view(),
        {}, 'edit-page'),
    re_path(r'^pages/instructor/(?P<path>.*)$',
        capsim.main.views.InstructorPage.as_view()),
    re_path(r'^pages/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
