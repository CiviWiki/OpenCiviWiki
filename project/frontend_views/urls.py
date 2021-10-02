from django.urls import path
from frontend_views import views

urlpatterns = [
    path("about/", views.about_view, name="about"),
    path("support_us/", views.support_us_view, name="support us"),
    path("howitworks/", views.how_it_works_view, name="how it works"),
    path("profile/<str:username>/", views.user_profile, name="profile"),
    path("thread/<int:thread_id>/", views.issue_thread, name="issue thread"),
    path("profile/", views.user_profile, name="default_profile"),
    path("", views.base_view, name="base"),
    path("thread/<int:thread_id>)/csv/", views.civi2csv, name="civi2csv"),
]
