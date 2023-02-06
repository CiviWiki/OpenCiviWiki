import factory

from .models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


categories = CategoryFactory.create_batch(10)
for category in categories:
    print(category.name)
