# flake8: noqa
from capsim.settings_shared import *

try:
    from capsim.local_settings import *
except ImportError:
    pass
