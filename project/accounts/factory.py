from turtle import color
import factory
from . import models
from categories.factory import CategoryFactory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    profile = factory.RelatedFactory(UserFactory, factory_related_name="profile")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    about_me = factory.Faker('sentence', nb_words=20)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of categores using bulk addition
        self.categories.add(*extracted)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        self.tags.add(u'abc, cde', u'xzy')

    @factory.post_generation
    def followers(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of following using bulk addition
        self.followers.add(*extracted)

    @factory.post_generation
    def following(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of following using bulk addition
        self.following.add(*extracted)

    is_verified = factory.Faker().pybool()
    full_profile = factory.Faker().pybool()
    profile_image = factory.django.ImageField(color='blue')
    profile_image_thumb = factory.django.ImageField(color='blue')
    
    #defining the ProfileManager for the objects field
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.summarize(*args, **kwargs)



    
    

    

