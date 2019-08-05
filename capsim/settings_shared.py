# Django settings for capsim project.
import os.path
import djcelery
import sys
from ccnmtlsettings.shared import common
import urllib3.contrib.pyopenssl

# Tell urllib3 to use pyOpenSSL. Needed by python < 2.7.9
# to resolve an SNIMissingWarning.
# See:
#   https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl-py2
#   https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
urllib3.contrib.pyopenssl.inject_into_urllib3()

project = 'capsim'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'capsim.main', 'capsim.sim'
]

USE_TZ = True

djcelery.setup_loader()

if 'test' in sys.argv or 'jenkins' in sys.argv:
    CELERY_ALWAYS_EAGER = True
    BROKER_BACKEND = 'memory'


INSTALLED_APPS += [  # noqa
    'django.contrib.humanize',
    'bootstrap3',
    'bootstrapform',
    'django_extensions',
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

BROKER_URL = "amqp://localhost:5672//capsim"
CELERYD_CONCURRENCY = 4

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
