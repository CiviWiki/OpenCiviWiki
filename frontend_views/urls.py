from django.conf.urls import url
import views as v

urlpatterns = [
    url(r'^dbview$', v.dbview, name='dbview'),
    url(r'^login$', v.login_view, name='login'),
    url(r'^beta$', v.beta_view, name='beta'),
    url(r'^about$', v.about_view, name='about'),
    url(r'^support_us$', v.support_us_view, name='support us'),
    url(r'^howitworks$', v.how_it_works_view, name='how it works'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_]*)$', v.user_profile, name='profile'),
    url(r'^thread/(?P<thread_id>\w+)$', v.issue_thread, name='issue thread'),
    url(r'^profile$', v.user_profile, name='default_profile'),
    url(r'^add_civi$', v.add_civi, name='add civi'),
    url(r'^$', v.base_view, name='base'),
    url(r'', v.does_not_exist, name='404')
]
