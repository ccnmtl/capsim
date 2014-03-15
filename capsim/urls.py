from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from pagetree.generic.views import PageView
import capsim.main.views
import capsim.sim.views
from capsim.sim.models import RunRecord, Experiment
admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    (r'^$', TemplateView.as_view(template_name="main/home.html")),
    (r'^contact/$', TemplateView.as_view(template_name="main/contact.html")),
    (r'^about/$', TemplateView.as_view(template_name="main/about.html")),
    (r'^topics/$', TemplateView.as_view(template_name="main/topics.html")),
    (r'^topic-obesity/$', TemplateView.as_view(
     template_name="sim/topic-obesity.html")),
    (r'^topic-obesity-debrief/$', TemplateView.as_view(
     template_name="sim/topic-obesity-debrief.html")),
    (r'^run/new/$', capsim.main.views.NewRunView.as_view()),
    (r'^run/$', capsim.sim.views.RunsView.as_view()),
    (r'^run/compare/$', capsim.sim.views.CompareRunsView.as_view()),
    (r'^run/toggle/$', capsim.main.views.ToggleFlagView.as_view()),
    (r'^run/(?P<id>\d+)/$', capsim.sim.views.RunView.as_view()),
    (r'^run/(?P<pk>\d+)/json/$', capsim.sim.views.RunOutputView.as_view()),
    (r'^run/(?P<pk>\d+)/edit/$', capsim.sim.views.RunEditView.as_view()),
    (r'^run/(?P<pk>\d+)/delete/$',
     DeleteView.as_view(model=RunRecord, success_url="/run/")),

    (r'^experiment/new/$', capsim.sim.views.NewExperimentView.as_view()),
    (r'^experiment/$', capsim.sim.views.ExperimentListView.as_view()),
    (r'^experiment/(?P<pk>\d+)/$', DetailView.as_view(model=Experiment)),
    (r'^experiment/(?P<pk>\d+)/csv/$',
     capsim.sim.views.ExperimentOutputView.as_view()),
    (r'^experiment/(?P<pk>\d+)/heatmap/$',
     DetailView.as_view(
         model=Experiment,
         template_name="sim/experiment_heatmap.html")),
    (r'^experiment/(?P<pk>\d+)/delete/$',
     capsim.sim.views.ExperimentDeleteView.as_view()),

    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/', TemplateView.as_view(template_name="stats.html")),
    (r'^model/', TemplateView.as_view(template_name="main/model.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^pages/edit/(?P<path>.*)$', capsim.main.views.EditPage.as_view(),
     {}, 'edit-page'),
    (r'^pages/instructor/(?P<path>.*)$',
     capsim.main.views.InstructorPage.as_view()),
    (r'^pages/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),
)
