from django.conf.urls import url
import authentication

urlpatterns = [
    url(r'^login', authentication.cw_login, name='login'),
    url(r'^logout', authentication.cw_logout, name='logout'),
    url(r'^register', authentication.cw_register, name='register')
]
