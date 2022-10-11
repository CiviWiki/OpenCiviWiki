from accounts import api
from django.urls import path

urlpatterns = [
    # TODO: port to Django view
    path("feed/", api.get_feed, name="get_feed"),
    # TODO: port to Django view
    path("deleteuser/", api.delete_user, name="delete_user"),
    # TODO: port to Django view
    path("upload_profile/", api.upload_profile_image, name="upload_profile"),
    # TODO: port to Django view
    path("follow/", api.request_follow, name="follow_user"),
    # TODO: port to Django view
    path("unfollow/", api.request_unfollow, name="unfollow_user"),
    # TODO: port to Django view
    path(
        "edit_user_categories/", api.edit_user_categories, name="edit_user_categories"
    ),
]
