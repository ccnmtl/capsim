# Django settings for capsim project.
import os.path
import sys
from ccnmtlsettings.shared import common


project = 'capsim'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'capsim.main', 'capsim.sim'
]

USE_TZ = True

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = "amqp://localhost:5672//capsim"
CELERY_WORKER_CONCURRENCY = 4

if 'test' in sys.argv or 'jenkins' in sys.argv:
    from celery.contrib.testing.app import DEFAULT_TEST_CONFIG

    CELERY_BROKER_URL = DEFAULT_TEST_CONFIG.get('broker_url')
    CELERY_RESULT_BACKEND = DEFAULT_TEST_CONFIG.get('result_backend')
    CELERY_BROKER_HEARTBEAT = DEFAULT_TEST_CONFIG.get('broker_heartbeat')


INSTALLED_APPS += [  # noqa
    'django.contrib.humanize',
    'bootstrap3',
    'bootstrapform',
    'django_extensions',
    'django_cas_ng',
    'pagetree',
    'pageblocks',
    'quizblock',
    'capsim.main',
    'capsim.sim',
    'sorl.thumbnail',
    'infranil',
    'django_celery_results',
]

INSTALLED_APPS.remove('djangowind') # noqa
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MIDDLEWARE += [  # noqa
    'django_cas_ng.middleware.CASMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend'
]

PAGEBLOCKS = ['pageblocks.TextBlock',
              'pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'pageblocks.ImageBlock',
              'pageblocks.ImagePullQuoteBlock',
              'quizblock.Quiz',
              ]

IPYTHON_ARGUMENTS = [
    '--pylab',
]

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
    ('intervention_health_promoting_food', 'medium'): dict(mass=-1.),

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

CAS_SERVER_URL = 'https://cas.columbia.edu/cas/'
CAS_VERSION = '3'
CAS_ADMIN_REDIRECT = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(base, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'stagingcontext.staging_processor',
                'gacontext.ga_processor'
            ],
        },
    },
]
