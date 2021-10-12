from django.urls import path
from threads import views


urlpatterns = [
    path("thread/<int:thread_id>/csv/", views.civi2csv, name="civi2csv"),
    path("thread/<int:thread_id>/", views.issue_thread, name="issue_thread"),
    path("about/", views.about_view, name="about"),
    path("support_us/", views.support_us_view, name="support us"),
    path("howitworks/", views.how_it_works_view, name="how it works"),
    path("declaration/", views.declaration, name="declaration"),
    path("create-group/", views.create_group, name="create group"),
    path("", views.base_view, name="base"),
]
