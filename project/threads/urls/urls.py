from django.urls import path
from ..views.views import (
    about_view,
    support_us_view,
    how_it_works_view,
    declaration,
    create_group,
    base_view,
)


urlpatterns = [
    path("about/", about_view, name="about"),
    path("", base_view, name="base"),
    path("support_us/", support_us_view, name="support us"),
    path("howitworks/", how_it_works_view, name="how it works"),
    path("declaration/", declaration, name="declaration"),
    path("create-group/", create_group, name="create group"),
]
