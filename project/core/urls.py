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

from core.router import CiviWikiRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(CiviWikiRouter.urls)),
    path("api/", include("threads.urls.api")),
    path("api/", include("threads.urls.graph_api")),
    path("", include("accounts.urls")),
    path("", include("threads.urls.urls")),
    path(
        "inbox/notifications/",
        include("notifications.urls", namespace="notifications"),
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
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("__debug__/", include("debug_toolbar.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
