from categories.api import CategoryViewSet
from rest_framework import routers
from threads.views import CiviViewSet, ThreadViewSet

CiviWikiRouter = routers.DefaultRouter()
CiviWikiRouter.register(r"categories", CategoryViewSet)
CiviWikiRouter.register(r"threads", ThreadViewSet)
CiviWikiRouter.register(r"civis", CiviViewSet)
