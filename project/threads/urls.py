from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .api import (create_civi, delete_civi, edit_civi, edit_thread, get_civi,
                  get_thread, rate_civi, upload_civi_image, new_thread, get_civis,
                  get_responses, upload_thread_image)

from .views import (
    ThreadViewSet, CategoryViewSet,
    CiviViewSet
)
from accounts.api import ProfileViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"threads", ThreadViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"civis", CiviViewSet)
router.register(r"accounts", ProfileViewSet)

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
    url(r"^new_thread/$", new_thread, name="new thread"),
    url(r"^edit_thread/$", edit_thread, name="edit thread"),
    url(r"^new_civi/$", create_civi, name="new civi"),
    url(r"^rate_civi/$", rate_civi, name="rate civi"),
    url(r"^edit_civi/$", edit_civi, name="edit civi"),
    url(r"^delete_civi/$", delete_civi, name="delete civi"),
    url(r"^upload_images/$", upload_civi_image, name="upload images"),
    url(r"^upload_image/$", upload_thread_image, name="upload image"),
]
