from capsim.settings_shared import *  # noqa F403
from ccnmtlsettings.staging import common
from django.conf import settings
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

locals().update(
    common(
        project=project,  # noqa F405
        base=base,  # noqa F405
        STATIC_ROOT=STATIC_ROOT,  # noqa F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa F405
        cloudfront="d1ygvzft7nlg5y",
    ))

try:
    from capsim.local_settings import *  # noqa F403
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa F405
        integrations=[DjangoIntegration()],
        debug=True,
    )
