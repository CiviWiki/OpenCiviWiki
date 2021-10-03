from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (RegisterView, SettingsView, ProfileActivationView, PasswordResetView, PasswordResetDoneView,
                            PasswordResetConfirmView, PasswordResetCompleteView, ProfileSetupView)
from accounts.views import user_profile

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/register/login.html'),
        name='accounts_login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='accounts_logout'),
    path('register/', RegisterView.as_view(), name='accounts_register'),
    path('settings/', SettingsView.as_view(), name='accounts_settings'),
    path('activate_account/<uidb64>/<token>/', ProfileActivationView.as_view(), name='accounts_activate'),
    path(
        'accounts/password_reset/',
        PasswordResetView.as_view(),
        name='accounts_password_reset',
    ),
    path(
        'accounts/password_reset_done/',
        PasswordResetDoneView.as_view(),
        name='accounts_password_reset_done',
    ),
    path(
        'accounts/password_reset_confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='accounts_password_reset_confirm',
    ),
    path(
        'accounts/password_reset_complete/',
        PasswordResetCompleteView.as_view(),
        name='accounts_password_reset_complete',
    ),
    path('setup/', ProfileSetupView.as_view(), name="accounts_profile_set[]"),
    path("profile/(?P<username>[a-zA-Z0-9-_]*)$", user_profile, name="profile"),
    path("profile/rep/(?P<username>\d+)$", user_profile, name="profile"),
    path("profile$", user_profile, name="default_profile"),

]


