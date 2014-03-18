from django.contrib.auth.models import User
from django.db import models
from json import dumps, loads
from .logic import Run, RunOutput
from .paramset import SimParamSet
import numpy as np
import pandas as pd


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

    def failed(self):
        self.status = "failed"
        self.save()

    def normalize_title(self):
        """ if the user doesn't set a title, we make one"""
        if len(self.title) > 0:
            return
        self.title = (
            "[(%s, %f - %f [%d]) x (%s, %f - %f [%d])] x %d trials" % (
                self.independent_variable,
                float(self.independent_min),
                float(self.independent_max),
                self.independent_steps,
                self.dependent_variable,
                float(self.dependent_min),
                float(self.dependent_max),
                self.dependent_steps,
                self.trials))
        self.save()

    def heatmap(self):
        data = []
        for er in self.exprun_set.all():
            data.append(dict(ind=er.independent_value, dep=er.dependent_value,
                             trial=er.trial, mass=er.mass))
        df = pd.DataFrame(data)
        hdict = df.groupby(['ind', 'dep'])['mass'].mean().to_dict()
        # since floats make bad dict keys, we force them to
        # string representations. This is reliable but arbitrarily
        # limits us to 4 decimal points of precision. Not perfect,
        # but probably good enough for generating a heatmap
        # in this context. Just beware that this heatmap function
        # will be buggy for very small or very large floating point
        # numbers. In those cases, you would probably want to use
        # a proper implementation from matplotlib or something
        # anyway. This is just for quick and dirty web heatmaps.
        fixed_dict = dict()
        for (i, j) in hdict.keys():
            fixed_dict[("%04f" % i, "%04f" % j)] = hdict[(i, j)]
        output = np.zeros((self.independent_steps, self.dependent_steps))
        ind_steps = make_steps(self.independent_min, self.independent_max,
                               self.independent_steps)
        dep_steps = make_steps(self.dependent_min, self.dependent_max,
                               self.dependent_steps)
        for i, i_step in enumerate(ind_steps):
            for j, j_step in enumerate(dep_steps):
                output[i][j] = fixed_dict[("%04f" % i_step, "%04f" % j_step)]
        return dict(data=output, min=np.min(output), max=np.max(output))


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
        self.mass = self.run.runoutput(
            ).get_runoutput().display_data()['mass_mean']
        self.save()
        self.experiment.check_if_complete()

    def failed(self):
        self.status = "failed"
        self.save()
        self.experiment.failed()


class Intervention(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)

    def get_absolute_url(self):
        return "/calibrate/intervention/%d/" % self.id

    def high_cost(self):
        return self.interventionlevel_set.filter(level="high")[0].cost

    def medium_cost(self):
        return self.interventionlevel_set.filter(level="medium")[0].cost

    def low_cost(self):
        return self.interventionlevel_set.filter(level="low")[0].cost

    def level_modifiers(self, level):
        return self.interventionlevel_set.filter(
            level=level)[0].modifier_set.all()

    def high_modifiers(self):
        return self.level_modifiers("high")

    def medium_modifiers(self):
        return self.level_modifiers("medium")

    def low_modifiers(self):
        return self.level_modifiers("low")

    def clear_all_modifiers(self):
        for il in self.interventionlevel_set.all():
            il.modifier_set.all().delete()

    def add_modifier(self, level, parameter, adjustment):
        il = self.interventionlevel_set.filter(level=level)[0]
        Modifier.objects.create(
            interventionlevel=il, parameter=parameter, adjustment=adjustment)


class InterventionLevel(models.Model):
    intervention = models.ForeignKey(Intervention)
    level = models.CharField(
        max_length=256,
        choices=[("high", "high"),
                 ("medium", "medium"),
                 ("low", "low")])
    cost = models.IntegerField(default=0)


class Modifier(models.Model):
    interventionlevel = models.ForeignKey(InterventionLevel)
    parameter = models.CharField(max_length=256)
    adjustment = models.FloatField(default=0.0)


class Parameter(models.Model):
    slug = models.SlugField(max_length=256)
    num_type = models.CharField(
        max_length=256,
        choices=[("float", "floating point"),
                 ("int", "integer")])
    value = models.FloatField(default=0.0)

    def get_absolute_url(self):
        return "/calibrate/parameter/%d/" % self.id

    def cast_value(self):
        if self.num_type == "int":
            return int(self.value)
        return self.value


def merge_parameters_into_form(form, parameters):
    for p in parameters:
        if p.slug in form.fields:
            form.fields[p.slug].initial = p.cast_value()
    return form
