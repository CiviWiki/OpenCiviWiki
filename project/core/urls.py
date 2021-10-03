"""civiwiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from threads import urls as threads
from frontend_views import urls as frontend_views
from core.router import CiviWikiRouter
from core.views.general_views import (
    landing_view,
    how_it_works_view,
    about_view,
    support_us_view,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls.urls")),
    path("api/", include("accounts.urls.api")),
    path("api/v1/", include((CiviWikiRouter.urls, "api"))),
    path("api/", include(threads)),
    path(
        "inbox/notifications/", include("notifications.urls", namespace="notifications")
    ),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon/favicon.ico")),
    path(
        "favicon-32x32.png",
        RedirectView.as_view(url="/static/favicon/favicon-32x32.png"),
    ),
    path(
        "apple-touch-icon.png",
        RedirectView.as_view(url="/static/favicon/apple-touch-icon.png"),
    ),
    path(
        "mstile-144x144.png",
        RedirectView.as_view(url="/static/favicon/mstile-144x144.png"),
    ),
    path("", include(frontend_views)),
]


# urlpatterns += [
#     path("", landing_view),
#     path("about", about_view),
#     path("howitworks", how_it_works_view),
#     path("support_us", support_us_view),
# ]
