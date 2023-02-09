import factory
import factory.fuzzy
from account.factory import ProfileFactory
from threads.factory import CiviFactory, ThreadFactory

from .models import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    account = factory.SubFactory(ProfileFactory)
    thread = factory.SubFactory(ThreadFactory)
    civi = factory.SubFactory(CiviFactory)
    activity_type = factory.Faker("lorem")
    read = factory.fuzzy.FuzzyChoice(choices=[True, True, True, False])
