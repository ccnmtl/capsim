from celery.decorators import task
from django_statsd.clients import statsd
from .models import Experiment, ExpRun, RunRecord, RunOutputRecord


@task
def run_experiment(experiment_id):
    statsd.incr("run_experiment")
    print "running experiment %d" % experiment_id
    e = Experiment.objects.get(id=experiment_id)
    e.populate(callback=process_run.delay)


@task
def process_run(run_id, exprun_id):
    statsd.incr("process_run")
    print "process_run %d, %d" % (run_id, exprun_id)
    rr = RunRecord.objects.get(id=run_id)
    r = rr.get_run()
    out = r.run()
    ror = RunOutputRecord(run=rr)
    ror.from_runoutput(out)
    er = ExpRun.objects.get(id=exprun_id)
    er.completed(ror)
