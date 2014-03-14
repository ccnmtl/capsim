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


class ExpRunFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ExpRun
    experiment = factory.SubFactory(ExperimentFactory)
    run = factory.SubFactory(RunRecordFactory)
