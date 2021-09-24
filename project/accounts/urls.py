from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from accounts.views import (RegisterView, SettingsView, ProfileActivationView, PasswordResetView, PasswordResetDoneView,
                            PasswordResetConfirmView, PasswordResetCompleteView, ProfileSetupView)
from accounts import api

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
    path('setup/', ProfileSetupView.as_view(), name="accounts_profile_setup"),
]


# REST endpoints
router = DefaultRouter(trailing_slash=False)
router.register(r"accounts", api.ProfileViewSet)

urlpatterns += [
    path('api/v1/', include(router.urls)),
]

urlpatterns += [
    path('api/v1/account_data/<str:username>/', api.get_user, name="get_user"),
    path('api/v1/account_profile/<str:username>/', api.get_profile, name="get_profile"),
    path('api/v1/account_card/<str:username>/', api.get_card, name="get_card"),
    path('api/v1/feed/', api.get_feed, name="get_feed"),
    path('api/v1/edituser/', api.edit_user, name="edit_user"),
    path('api/v1/upload_profile/', api.upload_profile_image, name="upload_profile"),
    path('api/v1/clear_profile/', api.clear_profile_image, name="clear_profile"),
    path('api/v1/follow/', api.request_follow, name="follow_user"),
    path('api/v1/unfollow/', api.request_unfollow, name="unfollow_user"),
    path('api/v1/edit_user_categories/', api.edit_user_categories, name="edit_user_categories"),
]
