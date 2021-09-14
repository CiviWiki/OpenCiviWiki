from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views
from . import authentication

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(template_name='accounts/register/login.html'),
        name='accounts_login',
    ),
    url(r"^logout", authentication.cw_logout, name="logout"),
    url(r"^register", authentication.cw_register, name="register"),
    url(
        r"^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        authentication.activate_view,
        name="activate_account",
    ),
    url(
        r"^forgot/$",
        views.PasswordResetView.as_view(),
        authentication.recover_user(),
        name="password_reset",
    ),
    url(
        r"^recovery_email_sent/$",
        authentication.recover_user_sent,
        name="recovery_email_sent",
    ),
    url(
        r"^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.PasswordResetConfirmView.as_view(),
        authentication.password_reset_confirm(),
        name="password_reset_confirm",
    ),
    url(
        r"^password_reset/done/$",
        authentication.password_reset_complete,
        name="password_reset_complete",
    ),
]
