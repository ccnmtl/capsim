# flake8: noqa
from settings_shared import *
from ccnmtlsettings.production import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        cloudfront="d1xa4pq0x5fm1x",
    ))

try:
    from local_settings import *
except ImportError:
    pass
