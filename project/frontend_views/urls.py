from django.conf.urls import url
from . import views as v

urlpatterns = [
    url(r"^about$", v.about_view, name="about"),
    url(r"^support_us$", v.support_us_view, name="support us"),
    url(r"^howitworks$", v.how_it_works_view, name="how it works"),
    url(r"^profile/(?P<username>[a-zA-Z0-9-_]*)$", v.user_profile, name="profile"),
    url(r"^profile/rep/(?P<username>\d+)$", v.user_profile, name="profile"),
    url(r"^thread/(?P<thread_id>\w+)$", v.issue_thread, name="issue thread"),
    url(r"^profile$", v.user_profile, name="default_profile"),
    url(r"^$", v.base_view, name="base"),
    url(r"^thread/(?P<thread_id>\w+)/csv$", v.civi2csv, name="civi2csv"),
]