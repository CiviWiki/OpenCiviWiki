from accounts import api
from django.urls import path

urlpatterns = [
    # TODO: port to Django view
    path("follow/", api.request_follow, name="follow_user"),
    # TODO: port to Django view
    path("unfollow/", api.request_unfollow, name="unfollow_user"),
]
