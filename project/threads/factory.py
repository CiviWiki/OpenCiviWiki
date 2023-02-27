import factory
import factory.fuzzy
from categories.factory import CategoryFactory
from django.contrib.auth.models import User

from .models import (
    Activity,
    Civi,
    CiviImage,
    Fact,
    Rationale,
    Rebuttal,
    Response,
    Thread,
)


class FactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fact

    body = factory.Faker("lorem")


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thread

    author = User.objects.get_or_create(username="admin")
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker("lorem")
    summary = factory.Faker("lorem")
    image = factory.Faker("image_url")
    is_draft = factory.fuzzy.FuzzyChoice(choices=[True, False])
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

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
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
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def objects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obje in extracted:
                self.objects.add(obje)


class ResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Response

    author = User.objects.get_or_create(username="admin")
    civi = factory.SubFactory(CiviFactory)
    title = factory.Faker("lorem")
    body = factory.Faker("lorem")
    votes_vneg = 0
    votes_neg = 0
    votes_neutral = 0
    votes_pos = 0
    votes_vpos = 0


class CiviImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CiviImage

    civi = factory.SubFactory(CiviFactory)
    title = factory.Faker("lorem")
    image = factory.Faker("image_url")

    @factory.post_generation
    def objects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obje in extracted:
                self.objects.add(obje)


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    user = factory.SubFactory("app.factories.UserFactory")
    thread = factory.SubFactory(ThreadFactory)
    civi = factory.SubFactory(CiviFactory)
    activity_type = factory.Faker("lorem")
    read = factory.fuzzy.FuzzyChoice(choices=[True, False])


class RebuttalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rebuttal

    author = User.objects.get_or_create(username="admin")
    response = factory.SubFactory(ResponseFactory)
    body = factory.Faker("lorem")
    votes_vneg = 0
    votes_neg = 0
    votes_neutral = 0
    votes_pos = 0
    votes_vpos = 0


class RationaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rationale

    title = factory.Faker("lorem")
    body = factory.Faker("lorem")
    votes_vneg = 0
    votes_neg = 0
    votes_neutral = 0
    votes_pos = 0
    votes_vpos = 0
