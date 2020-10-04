from django.conf.urls import url
from django.contrib.auth import views as auth_views
from authentication import authentication

urlpatterns = [
    url(r'^login', authentication.cw_login, name='login'),
    url(r'^logout', authentication.cw_logout, name='logout'),
    url(r'^register', authentication.cw_register, name='register'),
    url(r'^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        authentication.activate_view, name='activate_account'),
    url(r'^beta_register', authentication.beta_register, name='beta_register'),

    url(r'^forgot/$', auth_views.PasswordResetView.as_view(), authentication.recover_user(), name='password_reset'),
    url(r'^recovery_email_sent/$', authentication.recover_user_sent, name='recovery_email_sent'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), authentication.password_reset_confirm(),
        name='password_reset_confirm'),
    url(r'^password_reset/done/$', authentication.password_reset_complete, name='password_reset_complete')


]
