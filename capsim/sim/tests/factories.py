import factory
from django.contrib.auth.models import User
from capsim.sim.models import Experiment, RunRecord, ExpRun


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    is_staff = True


class RunRecordFactory(factory.DjangoModelFactory):
    FACTORY_FOR = RunRecord
    user = factory.SubFactory(UserFactory)


class ExperimentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Experiment
    user = factory.SubFactory(UserFactory)
    total = 1
    data = "{}"
    independent_min = 0.0
    independent_max = 1.0
    independent_steps = 1
    dependent_min = 0.0
    dependent_max = 1.0
    dependent_steps = 1
    trials = 1


class ExpRunFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ExpRun
    experiment = factory.SubFactory(ExperimentFactory)
    run = factory.SubFactory(RunRecordFactory)
