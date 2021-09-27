from core.router import CiviWikiRouter
from categories.api import CategoryViewSet

CiviWikiRouter.register(r'categories', CategoryViewSet)
