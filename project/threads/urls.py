from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views, read, write

router = DefaultRouter(trailing_slash=False)
router.register(r"threads", views.ThreadViewSet)
router.register(r"civis", views.CiviViewSet)

urlpatterns = [
    url(r"^v1/", include(router.urls)),
]

urlpatterns += [
    url(r"^thread_data/(?P<thread_id>\w+)/$", read.get_thread, name="get thread"),
    url(r"^civi_data/(?P<civi_id>\w+)$", read.get_civi, name="get civi"),
    url(r"^threads/(?P<thread_id>\w+)/civis$", read.get_civis, name="get civis"),
    url(
        r"^response_data/(?P<thread_id>\w+)/(?P<civi_id>\w+)/$",
        read.get_responses,
        name="get responses",
    ),
    url(r"^feed/$", read.get_feed, name="get thread"),
    url(r"^new_thread/$", write.new_thread, name="new thread"),
    url(r"^edit_thread/$", write.editThread, name="edit thread"),
    url(r"^new_civi/$", write.createCivi, name="new civi"),
    url(r"^rate_civi/$", write.rateCivi, name="rate civi"),
    url(r"^edit_civi/$", write.editCivi, name="edit civi"),
    url(r"^delete_civi/$", write.deleteCivi, name="delete civi"),
]
