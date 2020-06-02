from __future__ import absolute_import, unicode_literals
from celery import Celery, signals

app = Celery('capsim')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


app.log.setup()
