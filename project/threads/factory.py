from turtle import title
import factory
from . import models
from shared_factory.shared_factory import FreezeTimeModelFactory
from accounts.factory import UserFactory
from categories.factory import CategoryFactory
from core.constants import CIVI_TYPES

class FactFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Fact
    
    body = factory.Faker('sentence', nb_words=100)


class ThreadFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Thread

    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def facts(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return
        # Add the iterable of categores using bulk addition
        self.facts.add(*extracted)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        self.tags.add(u'abc, cde', u'xzy')
    
    title = factory.Faker('sentence', nb_words= 4)
    summary = factory.Faker('sentence', nb_words= 30)
    image = factory.django.ImageField(color='blue')
    is_draft = factory.Faker().pybool()
    num_views = factory.fuzzy.FuzzyInteger(0, 30)
    num_civis = factory.fuzzy.FuzzyInteger(0, 30)
    num_solutions = factory.fuzzy.FuzzyInteger(0, 30)

    #defining the ThreadManager for the objects field
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.summarize(*args, **kwargs)


class CiviFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Civi

    authors = factory.SubFactory(UserFactory)
    thread = factory.SubFactory(ThreadFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        self.tags.add(u'abc, cde', u'xzy')

    @factory.post_generation
    def linked_civis(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return
        # Add the iterable of following using bulk addition
        self.linked_civis.add(*extracted)

    title = factory.Faker('sentence', nb_words= 4)
    body = factory.Faker('sentence', nb_words= 100)
    c_type = factory.fuzzy.FuzzyChoice(CIVI_TYPES, getter=lambda c: c[0])
    votes_vneg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neutral = factory.fuzzy.FuzzyInteger(0, 30)
    votes_pos = factory.fuzzy.FuzzyInteger(0, 30)
    votes_vpos = factory.fuzzy.FuzzyInteger(0, 30)

    #Please verify if this is the right implementation for votes = property(_get_votes)
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        votes = model_class(*args, **kwargs)
        return votes._get_votes()

    #defining the CiViManager for the objects field
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.summarize(*args, **kwargs)


class ResponseFactory(factory.Factory):
    class Meta:
        model = models.Response

    author = factory.SubFactory(UserFactory)
    civi = factory.SubFactory(CiviFactory)
    title = factory.Faker('sentence', nb_words= 4)
    body = factory.Faker('sentence', nb_words= 100)
    votes_vneg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neutral = factory.fuzzy.FuzzyInteger(0, 30)
    votes_pos = factory.fuzzy.FuzzyInteger(0, 30)
    votes_vpos = factory.fuzzy.FuzzyInteger(0, 30)


class CiviImageFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.CiviImage

    civi = factory.SubFactory(CiviFactory)
    title = factory.Faker('sentence', nb_words= 4)
    image = factory.django.ImageField(color='blue')


    #defining the CiViManager for the objects field
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.get_images(*args, **kwargs)


class ActivityFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Activity

    user = factory.SubFactory(UserFactory)
    thread = factory.SubFactory(ThreadFactory)
    civi = factory.SubFactory(CiviFactory)
    activity_type = factory.fuzzy.FuzzyChoice(models.Activity.activity_CHOICES)
    read = factory.Faker().pybool()


class RebuttalFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Rebuttal

    author = factory.SubFactory(UserFactory)
    response = factory.SubFactory(ResponseFactory)
    body = factory.Faker('sentence', nb_words= 100)
    votes_vneg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neutral = factory.fuzzy.FuzzyInteger(0, 30)
    votes_pos = factory.fuzzy.FuzzyInteger(0, 30)
    votes_vpos = factory.fuzzy.FuzzyInteger(0, 30)


class RationaleFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Rationale

    title = factory.Faker('sentence', nb_words= 4)
    body = factory.Faker('sentence', nb_words= 100)
    votes_vneg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neg = factory.fuzzy.FuzzyInteger(0, 30)
    votes_neutral = factory.fuzzy.FuzzyInteger(0, 30)
    votes_pos = factory.fuzzy.FuzzyInteger(0, 30)
    votes_vpos = factory.fuzzy.FuzzyInteger(0, 30)

