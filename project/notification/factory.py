import factory
from . import models
from shared_factory.shared_factory import FreezeTimeModelFactory
from accounts.factory import ProfileFactory
from threads.factory import ThreadFactory, CiviFactory

class NotificationFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Notification

    account = factory.SubFactory(ProfileFactory)
    thread = factory.SubFactory(ThreadFactory)
    civi = factory.SubFactory(CiviFactory)
    activity_type = factory.fuzzy.FuzzyChoice(models.Notification.activity_CHOICES, getter=lambda c: c[0])
    read = factory.Faker().pybool()


