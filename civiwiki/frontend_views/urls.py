from django.conf.urls import url
import views as v

urlpatterns = [
    url(r'^creategroup$', v.create_group, name='add group'),
    url(r'^dbview$', v.dbview, name='dbview'),
    url(r'^login$', v.login_view, name='login'),
    url(r'^beta$', v.beta_view, name='beta'),
    url(r'^landing$', v.landing_view, name='landing'),
    url(r'^about$', v.about_view, name='about'),
    url(r'^support_us$', v.support_us_view, name='support us'),
    url(r'^howitworks$', v.how_it_works_view, name='how it works'),
    url(r'^account$', v.account_home, name='account home'),
    url(r'^add_civi$', v.add_civi, name='add civi'),
    url(r'^$', v.feed, name='feed'),
    url(r'', v.does_not_exist, name='404')
]
