"""civiwiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import django.contrib.auth.views as auth_views

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.views.static import serve
from django.views.generic.base import RedirectView

from api import urls as api
from accounts import urls as accounts_urls
from accounts.views import (RegisterView, PasswordResetView, PasswordResetDoneView,
                            PasswordResetConfirmView, PasswordResetCompleteView, settings_view)
from frontend_views import urls as frontend_views



urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^api/", include(api)),
    url(r"^auth/", include(accounts_urls)),

    # New accounts paths. These currently implement user registration/authentication in
    # parallel to the current authentication.
    path('accounts/register', RegisterView.as_view(), name='accounts_register'),
    path(
        'accounts/login',
        auth_views.LoginView.as_view(template_name='accounts/register/login.html'),
        name='accounts_login',
    ),

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
    url(r"^settings$",settings_view, name="settings"),
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
