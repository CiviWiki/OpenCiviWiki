import factory
from . import models
from shared_factory.shared_factory import FreezeTimeModelFactory

class CategoryFactory(FreezeTimeModelFactory):
    class Meta:
        model = models.Category

    name = factory.Iterator(["Politics","Voting","Referendum"])


