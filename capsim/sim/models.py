from django.db import models
from json import dumps, loads
from .logic import Run


class RunRecord(models.Model):
    created = models.DateTimeField(auto_now=True)
    data = models.TextField(default=u"", blank=True, null=True)

    def get_run(self):
        return Run.from_dict(loads(self.data))

    def from_run(self, run):
        self.data = dumps(run.to_dict())
        self.save()
