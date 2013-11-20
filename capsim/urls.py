from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import capsim.main.views
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
    (r'^$', capsim.main.views.IndexView.as_view()),
    (r'^run/$', 'capsim.sim.views.runs'),
    (r'^run/(?P<id>\d+)/$', 'capsim.sim.views.run'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/', TemplateView.as_view(template_name="stats.html")),
    (r'^model/', TemplateView.as_view(template_name="main/model.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^pages/edit/(?P<path>.*)$', 'capsim.main.views.edit_page',
     {}, 'edit-page'),
    (r'^pages/instructor/(?P<path>.*)$',
     'capsim.main.views.instructor_page'),
    (r'^pages/(?P<path>.*)$', 'capsim.main.views.page'),
)
