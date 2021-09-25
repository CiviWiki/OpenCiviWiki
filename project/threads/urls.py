from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .api import *
from .serializers import ThreadViewSet,CiviViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"threads", ThreadViewSet)
router.register(r"civis", CiviViewSet)

urlpatterns = [
    url(r"^v1/", include(router.urls)),
]

urlpatterns += [
    url(r"^thread_data/(?P<thread_id>\w+)/$", get_thread, name="get thread"),
    url(r"^civi_data/(?P<civi_id>\w+)$", get_civi, name="get civi"),
    url(r"^threads/(?P<thread_id>\w+)/civis$", get_civis, name="get civis"),
    url(
        r"^response_data/(?P<thread_id>\w+)/(?P<civi_id>\w+)/$",
        get_responses,
        name="get responses",
    ),
    url(r"^feed/$", get_feed, name="get thread"),
    url(r"^new_thread/$", new_thread, name="new thread"),
    url(r"^edit_thread/$", edit_thread, name="edit thread"),
    url(r"^new_civi/$", create_civi, name="new civi"),
    url(r"^rate_civi/$", rate_civi, name="rate civi"),
    url(r"^edit_civi/$", edit_civi, name="edit civi"),
    url(r"^delete_civi/$", delete_civi, name="delete civi"),
]
