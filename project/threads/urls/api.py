from django.urls import path
from threads import api


urlpatterns = [
    path("thread_data/<int:thread_id>/", api.get_thread, name="get thread"),
    path("civi_data/<int:civi_id>/", api.get_civi, name="get civi"),
    path("threads/<int:thread_id>/civis", api.get_civis, name="get civis"),
    path(
        "response_data/<int:thread_id>/<int:civi_id>/",
        api.get_responses,
        name="get responses",
    ),
    path("new_thread/", api.new_thread, name="new thread"),
    path("edit_thread/", api.edit_thread, name="edit thread"),
    path("new_civi/", api.create_civi, name="new civi"),
    path("rate_civi/", api.rate_civi, name="rate civi"),
    path("edit_civi/", api.edit_civi, name="edit civi"),
    path("delete_civi/", api.delete_civi, name="delete civi"),
    path("upload_images/", api.upload_civi_image, name="upload images"),
    path("upload_image/", api.upload_thread_image, name="upload image"),
]
