from accounts.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    ProfileActivationView,
    ProfileFollow,
    ProfileUnfollow,
    RegisterView,
    SettingsView,
    UserProfileView,
    expunge_user,
)
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/register/login.html"),
        name="accounts_login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="accounts_logout"),
    path("register/", RegisterView.as_view(), name="accounts_register"),
    path("settings/", SettingsView.as_view(), name="accounts_settings"),
    path(
        "activate_account/<uidb64>/<token>/",
        ProfileActivationView.as_view(),
        name="accounts_activate",
    ),
    path("profile/<str:username>/", UserProfileView.as_view(), name="profile"),
    path(
        "profile/<str:username>/follow", ProfileFollow.as_view(), name="profile-follow"
    ),
    path(
        "profile/<str:username>/unfollow",
        ProfileUnfollow.as_view(),
        name="profile-unfollow",
    ),
    path(
        "accounts/password_reset/",
        PasswordResetView.as_view(),
        name="accounts_password_reset",
    ),
    path(
        "accounts/password_reset_done/",
        PasswordResetDoneView.as_view(),
        name="accounts_password_reset_done",
    ),
    path(
        "accounts/password_reset_confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="accounts_password_reset_confirm",
    ),
    path(
        "accounts/password_reset_complete/",
        PasswordResetCompleteView.as_view(),
        name="accounts_password_reset_complete",
    ),
    path("accounts/expunge/", expunge_user, name="expunge_user"),
]
