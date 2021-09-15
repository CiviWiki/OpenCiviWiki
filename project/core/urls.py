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

from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic.base import RedirectView

from api import urls as api
from accounts.views import (PasswordResetView, PasswordResetDoneView,
                            PasswordResetConfirmView, PasswordResetCompleteView, settings_view)
from frontend_views import urls as frontend_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('accounts.urls')),
    url(r"^api/", include(api)),
    path(
        'accounts/password_reset',
        PasswordResetView.as_view(),
        name='accounts_password_reset',
    ),

    path(
        'accounts/password_reset_done',
        PasswordResetDoneView.as_view(),
        name='accounts_password_reset_done',
    ),
    path(
        'accounts/password_reset_confirm/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(),
        name='accounts_password_reset_confirm',
    ),

    path(
        'accounts/password_reset_complete',
        PasswordResetCompleteView.as_view(),
        name='accounts_password_reset_complete',
    ),
    url(r"^settings$", settings_view, name="settings"),
    url(
        "^inbox/notifications/",
        include("notifications.urls", namespace="notifications"),
    ),
]

urlpatterns += [
    # A redirect for favicons at the root of the site
    url(r"^favicon\.ico$", RedirectView.as_view(url="/static/favicon/favicon.ico")),
    url(
        r"^favicon-32x32\.png$",
        RedirectView.as_view(url="/static/favicon/favicon-32x32.png"),
    ),
    url(
        r"^apple-touch-icon\.png$",
        RedirectView.as_view(url="/static/favicon/apple-touch-icon.png"),
    ),
    url(
        r"^mstile-144x144\.png$",
        RedirectView.as_view(url="/static/favicon/mstile-144x144.png"),
    ),
    # Media and Static file Serve Setup.
    url(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    url(r"^", include(frontend_views)),

]
