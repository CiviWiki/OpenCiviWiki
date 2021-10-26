from rest_framework import routers
from accounts.api import ProfileViewSet
from categories.api import CategoryViewSet
from threads.views import CiviViewSet, ThreadViewSet


CiviWikiRouter = routers.DefaultRouter()
CiviWikiRouter.register(r"accounts", ProfileViewSet)
CiviWikiRouter.register(r"categories", CategoryViewSet)
CiviWikiRouter.register(r"threads", ThreadViewSet)
CiviWikiRouter.register(r"civis", CiviViewSet)
