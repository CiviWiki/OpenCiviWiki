from django.urls import path
from threads import views


urlpatterns = [
    path("thread/<int:thread_id>/csv/", views.civi2csv, name="civi2csv"),
    path("thread/<int:thread_id>/", views.issue_thread, name="issue_thread"),
    path("thread/", views.issue_thread, name="issue_thread"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("support_us/", views.SupportUsView.as_view(), name="support_us"),
    path("howitworks/", views.HowItWorksView.as_view(), name="how_it_works"),
    path("declaration/", views.DeclarationView.as_view(), name="declaration"),
    path("create-group/", views.create_group, name="create_group"),
    path("", views.base_view, name="base"),
]
