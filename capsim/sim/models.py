from django.contrib.auth.models import User
from django.db import models
from json import dumps, loads
from .logic import Run, RunOutput
from .paramset import SimParamSet


class RunRecord(models.Model):
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    data = models.TextField(default=u"", blank=True, null=True)
    title = models.TextField(default=u"", blank=True, null=True)
    description = models.TextField(default=u"", blank=True, null=True)

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


class Experiment(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField(default=u"", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=256, default="enqueued")

    data = models.TextField(default=u"", blank=True, null=True)

    independent_variable = models.CharField(max_length=256, default="",
                                            blank=True, null=True)
    dependent_variable = models.CharField(max_length=256, default="",
                                          blank=True, null=True)

    independent_min = models.FloatField(blank=True, null=True)
    independent_max = models.FloatField(blank=True, null=True)
    independent_steps = models.IntegerField(default=1, blank=True, null=True)

    dependent_min = models.FloatField(blank=True, null=True)
    dependent_max = models.FloatField(blank=True, null=True)
    dependent_steps = models.IntegerField(default=1, blank=True, null=True)

    trials = models.IntegerField(default=1)

    total = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)

    def get_absolute_url(self):
        return "/experiment/%d/" % self.id

    def populate(self, callback=None):
        """ make a run / exprun for each each step and queue them up """
        ind_steps = make_steps(self.independent_min, self.independent_max,
                               self.independent_steps)
        dep_steps = make_steps(self.dependent_min, self.dependent_max,
                               self.dependent_steps)
        parameters = loads(self.data)
        for trial in range(self.trials):
            for i in ind_steps:
                for j in dep_steps:
                    parameters[self.independent_variable] = i
                    parameters[self.dependent_variable] = j
                    rr = RunRecord.objects.create(
                        user=self.user,
                        data=dumps(parameters)
                        )
                    er = ExpRun.objects.create(
                        experiment=self,
                        run=rr,
                        status="enqueued",
                        independent_value=i,
                        dependent_value=j,
                        trial=trial,
                        )
                    if callback:
                        callback(run_id=rr.id, exprun_id=er.id)

        self.status = "processing"
        self.save()

    def check_if_complete(self):
        # need to make sure this isn't a race condition
        completed = self.exprun_set.filter(status="complete").count()
        self.completed = completed
        if completed == self.total:
            self.status = "complete"
        self.save()


def make_steps(min_value, max_value, num_steps):
    assert min_value < max_value
    num_steps = int(num_steps)
    assert num_steps > 0
    interval = max_value - min_value
    step_size = float(interval) / num_steps
    steps = [min_value + (s * step_size)
             for s in range(num_steps)]
    assert len(steps) == num_steps
    return steps


class ExpRun(models.Model):
    experiment = models.ForeignKey(Experiment)
    run = models.ForeignKey(RunRecord)

    status = models.CharField(max_length=256, default="enqueued")

    independent_value = models.FloatField(blank=True, null=True)
    dependent_value = models.FloatField(blank=True, null=True)

    trial = models.IntegerField(default=0)
    mass = models.FloatField(default="100.0")

    def completed(self, ror):
        self.status = "complete"
        self.save()
        # TODO: set mass
        self.experiment.check_if_complete()
