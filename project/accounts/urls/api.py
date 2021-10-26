from django.urls import path
from accounts import api

urlpatterns = [
    path("account_data/<str:username>/", api.get_user, name="get_user"),
    path("account_profile/<str:username>/", api.get_profile, name="get_profile"),
    path("account_card/<str:username>/", api.get_card, name="get_card"),
    path("feed/", api.get_feed, name="get_feed"),
    path("edituser/", api.edit_user, name="edit_user"),
    path("upload_profile/", api.upload_profile_image, name="upload_profile"),
    path("clear_profile/", api.clear_profile_image, name="clear_profile"),
    path("follow/", api.request_follow, name="follow_user"),
    path("unfollow/", api.request_unfollow, name="unfollow_user"),
    path(
        "edit_user_categories/", api.edit_user_categories, name="edit_user_categories"
    ),
]
