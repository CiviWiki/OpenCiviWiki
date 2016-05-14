from django.conf.urls import url
import views as v

urlpatterns = [
    url(r'^creategroup$', v.create_group, name='add group'),
    url(r'^dbview$', v.dbview, name='dbview'),
    url(r'^login$', v.login_view, name='login'),
    url(r'^supportus$', v.support_us_view, name='support us'),
    url(r'^beta$', v.beta_view, name='beta'),
    url(r'^about$', v.about_view, name='about'),
    url(r'^account$', v.account_home, name='account home'),
    url(r'^add_civi$', v.add_civi, name='add civi'),
    url(r'^$', v.account_home, name='home'),
    url(r'', v.does_not_exist, name='404')
]
