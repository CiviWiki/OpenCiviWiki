from django.conf.urls import include
from django.urls import path
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
    path("v1/", include(router.urls)),
]

urlpatterns += [
    path("thread_data/<int:thread_id>/", get_thread, name="get thread"),
    path("civi_data/<int:civi_id>/", get_civi, name="get civi"),
    path("threads/<int:thread_id>/civis", get_civis, name="get civis"),
    path(
        "response_data/<int:thread_id>/<int:civi_id>/",
        get_responses,
        name="get responses",
    ),
    path("new_thread/", new_thread, name="new thread"),
    path("edit_thread/", edit_thread, name="edit thread"),
    path("new_civi/", create_civi, name="new civi"),
    path("rate_civi/", rate_civi, name="rate civi"),
    path("edit_civi/", edit_civi, name="edit civi"),
    path("delete_civi/", delete_civi, name="delete civi"),
    path("upload_images/", upload_civi_image, name="upload images"),
    path("upload_image/", upload_thread_image, name="upload image"),
]
