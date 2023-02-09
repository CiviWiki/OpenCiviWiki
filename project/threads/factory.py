import factory
import factory.fuzzy
from categories.factory import CategoryFactory
from django.contrib.auth.models import User

from .models import Civi, Fact, Thread


class FactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fact

    body = factory.Sequence(lambda n: "Fact #%s" % n)


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thread

    author = User.objects.get_or_create(username="admin")
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker("lorem")
    summary = factory.Faker("lorem")
    image = factory.Faker("image_url")
    is_draft = factory.fuzzy.FuzzyChoice(choices=[True, True, True, True])
    num_views = 0
    num_civis = 0
    num_solutions = 0

    @factory.post_generation
    def facts(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for fact in extracted:
                self.facts.add(fact)

    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    def objects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obje in extracted:
                self.objects.add(obje)


class CiviFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Civi

    author = User.objects.get_or_create(username="admin")
    thread = factory.SubFactory(ThreadFactory)
    title = factory.Faker("lorem")
    body = factory.Faker("lorem")
    c_type = factory.Faker("lorem")
    votes_vneg = 0
    votes_neg = 0
    votes_neutral = 0
    votes_pos = 0
    votes_vpos = 0

    @factory.post_generation
    def linked_civis(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for linked_civi in extracted:
                self.linked_civis.add(linked_civi)

    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    def objects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obje in extracted:
                self.objects.add(obje)
