# Django settings for capsim project.
import os.path
import sys
import djcelery

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'capsim',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }
    CELERY_ALWAYS_EAGER = True
    BROKER_BACKEND = 'memory'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=capsim',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
)
PROJECT_APPS = [
    'capsim.main', 'capsim.sim'
]

ALLOWED_HOSTS = ['localhost', '.ccnmtl.columbia.edu']

USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/capsim/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'stagingcontext.staging_processor',
    'gacontext.ga_processor',
    'django.core.context_processors.static',
    'djangowind.context.context_processor',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'capsim.urls'

TEMPLATE_DIRS = (
    "/var/www/capsim/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

djcelery.setup_loader()

INSTALLED_APPS = [
    'gunicorn',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_markwhat',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.humanize',
    'typogrify',
    'django_nose',
    'compressor',
    'django_statsd',
    'bootstrapform',
    'debug_toolbar',
    'waffle',
    'django_jenkins',
    'smoketest',
    'django_extensions',
    'impersonate',
    'pagetree',
    'pageblocks',
    'quizblock',
    'capsim.main',
    'capsim.sim',
    'djcelery',
    'sorl.thumbnail',
    'infranil',
]

PAGEBLOCKS = ['pageblocks.TextBlock',
              'pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'pageblocks.ImageBlock',
              'pageblocks.ImagePullQuoteBlock',
              'quizblock.Quiz',
              ]

BROKER_URL = "amqp://localhost:5672//dmt"
CELERYD_CONCURRENCY = 4

INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
)

IPYTHON_ARGUMENTS = [
    '--pylab',
]

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'capsim'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[capsim] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "capsim@ccnmtl.columbia.edu"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

# CAS settings
AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend', )
CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', 'jb2410', 'zm4', 'egr2107',
                                'sld2131', 'amm8', 'mar227', 'jed2161']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
LOGIN_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

INTERVENTION_SKEWS = {
    # 1-2: Provide and Support Community Programs Designed
    #      to Increase Physical Activity
    ('intervention_increase_physical_activity', 'high'): dict(mass=-2.),
    ('intervention_increase_physical_activity', 'medium'): dict(mass=-1.),

    # 4-1:  Provide Standardized Care and Advocate for Healthy
    #       Community Environments
    ('intervention_ensure_screening', 'high'): dict(mass=-5.),
    ('intervention_ensure_screening', 'medium'): dict(mass=-3.),
    ('intervention_ensure_screening', 'low'): dict(mass=-1.),

    # 4-3: Encourage Active Living at Work
    ('intervention_active_living_at_work', 'high'): dict(mass=-2.),
    ('intervention_active_living_at_work', 'medium'): dict(mass=-1.),

    # 1-1:  Enhance the Physical and Built Environment
    ('intervention_physical_environment', 'high'): dict(mass=-2.),
    ('intervention_physical_environment', 'medium'): dict(mass=-1.),

    # Social Influence (Gamma 6)
    ('intervention_social_influence', 'high'): dict(mass=-4.),
    ('intervention_social_influence', 'medium'): dict(mass=-2.),

    # 2-4:  Introduce, Modify, and Utilize Health-Promoting
    #       Food and Beverage Retailing and Distribution Policies
    ('intervention_health_promoting_food', 'high'): dict(mass=-2.),
    ('intervention_health_promoting_food', 'high'): dict(mass=-1.),

    # 4-3: Encourage Active Living and Healthy Eating at Work
    ('intervention_healthy_eating_at_work', 'high'): dict(mass=-3.),
    ('intervention_healthy_eating_at_work', 'medium'): dict(mass=-2.),
    ('intervention_healthy_eating_at_work', 'low'): dict(mass=-1.),

    # 2-1:  Adopt Policies and Implement Practices to Reduce
    #       Overconsumption of Sugar-Sweetened Beverages
    ('intervention_national_health_standards', 'high'): dict(mass=-2.),
    ('intervention_national_health_standards', 'medium'): dict(mass=-1.),

    # 3-4: Adopt Consistent Nutrition Education Policies for Federal
    #      Programs with Nutrition Education Components
    ('intervention_nutrition_education_policies', 'high'): dict(mass=-3.),
    ('intervention_nutrition_education_policies', 'medium'): dict(mass=-2.),
    ('intervention_nutrition_education_policies', 'low'): dict(mass=-1.),

    # 3-3:  Ensure Consistent Nutrition Labeling for the Front of
    #       Packages, Retail Store Shelves, and Menus and Menu Boards
    #       That Encourages Healthier Food Choices
    ('intervention_food_labeling', 'high'): dict(mass=-2.),
    ('intervention_food_labeling', 'medium'): dict(mass=-1.),

    # Social Influence (Gamma 5)
    ('intervention_food_social_influence', 'high'): dict(mass=-4.),
    ('intervention_food_social_influence', 'medium'): dict(mass=-2.),
}
