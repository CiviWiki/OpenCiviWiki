from accounts import api
from django.urls import path

urlpatterns = [
    path("feed/", api.get_feed, name="get_feed"),
    path("edituser/", api.edit_user, name="edit_user"),
    path("deleteuser/", api.delete_user, name="delete_user"),
    path("upload_profile/", api.upload_profile_image, name="upload_profile"),
    path("follow/", api.request_follow, name="follow_user"),
    path("unfollow/", api.request_unfollow, name="unfollow_user"),
    path(
        "edit_user_categories/", api.edit_user_categories, name="edit_user_categories"
    ),
]
