# flake8: noqa
from capsim.settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        cloudfront="d1ygvzft7nlg5y",
    ))

try:
    from capsim.local_settings import *
except ImportError:
    pass
