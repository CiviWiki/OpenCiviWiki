from django.urls import path
from frontend_views.views import (
    about_view,
    support_us_view,
    how_it_works_view,
    issue_thread,
    civi2csv,
    base_view,
)

urlpatterns = [
    path("about/", about_view, name="about"),
    path("support_us/", support_us_view, name="support us"),
    path("howitworks/", how_it_works_view, name="how it works"),
    path("thread/<int:thread_id>/", issue_thread, name="issue thread"),
    path("", base_view, name="base"),
    path("thread/<int:thread_id>/csv/", civi2csv, name="civi2csv"),
]
