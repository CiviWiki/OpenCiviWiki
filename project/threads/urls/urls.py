from django.urls import path
from threads import views

urlpatterns = [
    path("thread/<int:thread_id>/csv/", views.civi2csv, name="civi2csv"),
    path("thread/<int:pk>/", views.ThreadDetailView.as_view(), name="thread-detail"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("support_us/", views.SupportUsView.as_view(), name="support-us"),
    path("howitworks/", views.HowItWorksView.as_view(), name="how-it-works"),
    path("declaration/", views.DeclarationView.as_view(), name="declaration"),
    path("create-group/", views.create_group, name="create-group"),
    path("feeds/", views.feeds, name="feeds"),
    path("", views.base_view, name="base"),
]
