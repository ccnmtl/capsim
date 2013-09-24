from django.db import models
from json import dumps, loads
from .logic import Run, RunOutput
from .paramset import SimParamSet


class RunRecord(models.Model):
    created = models.DateTimeField(auto_now=True)
    data = models.TextField(default=u"", blank=True, null=True)

    def get_run(self):
        return Run.from_dict(loads(self.data or '{}'))

    def from_run(self, run):
        self.data = dumps(run.to_dict())
        self.save()

    def get_absolute_url(self):
        return "/run/%d/" % self.id

    def runoutput(self):
        return self.runoutputrecord_set.all()[0]

    def params(self):
        return Run.from_dict(loads(self.data or '{}')).params

    def view_params(self):
        """ returns list of all parameters used for the model,
        with distinction drawn between the defaults and
        ones explicitly set """
        set_params = self.params()
        print str(set_params)
        all_params = SimParamSet(**set_params)
        d = all_params.to_dict()
        for k in d.keys():
            yield ViewParam(k, d[k], k not in set_params.keys())


class ViewParam(object):
    def __init__(self, name, value, default=True):
        self.name = name
        self.value = value
        self.default = default


class RunOutputRecord(models.Model):
    created = models.DateTimeField(auto_now=True)
    run = models.ForeignKey(RunRecord)
    data = models.TextField(default=u"", blank=True, null=True)

    def from_runoutput(self, runoutput):
        self.data = dumps(runoutput.to_dict())
        self.save()

    def get_runoutput(self):
        d = loads(self.data or '{}')
        run = self.run.get_run()
        return RunOutput(
            ticks=d.get('ticks', 1),
            params=run.params,
            data=loads(d.get('data', "{}")))
