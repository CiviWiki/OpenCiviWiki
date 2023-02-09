import factory
import factory.fuzzy
from django.contrib.auth.models import User

from .modes import Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("sentence", nb_words=20)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory("app.factories.UserFactory")
    first_name = factory.Faker("lorem")
    last_name = factory.Faker("lorem")
    about_me = factory.Faker("lorem")
    is_verified = factory.fuzzy.FuzzyChoice(choices=[False, False])
    profile_image = factory.Faker("image_url")
    profile_image_thumb = factory.Faker("image_url")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def following(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for follower in extracted:
                self.following.add(follower)
