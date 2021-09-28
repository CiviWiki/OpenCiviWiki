from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


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
        read.get_responses,
        name="get responses",
    ),
    url(r"^new_thread/$", new_thread, name="new thread"),
    url(r"^edit_thread/$", editThread, name="edit thread"),
    url(r"^new_civi/$", createCivi, name="new civi"),
    url(r"^rate_civi/$", rateCivi, name="rate civi"),
    url(r"^edit_civi/$", editCivi, name="edit civi"),
    url(r"^delete_civi/$", deleteCivi, name="delete civi"),
    url(r"^upload_images/$", uploadCiviImage, name="upload images"),
    url(r"^upload_image/$", uploadThreadImage, name="upload image"),
]
