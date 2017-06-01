from django.conf.urls import url
import authentication

urlpatterns = [
    url(r'^login', authentication.cw_login, name='login'),
    url(r'^logout', authentication.cw_logout, name='logout'),
    url(r'^register', authentication.cw_register, name='register'),
    url(r'^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', authentication.activate_view, name='activate_account'),
]
