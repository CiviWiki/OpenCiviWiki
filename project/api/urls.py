from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from api import views, read, write


router = DefaultRouter()
router.register(r'threads', views.ThreadViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'civis', views.CiviViewSet)

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='CiviWiki API', public=True)),
    url(r'^v1/', include(router.urls)),
]

urlpatterns += [
    url(r'^account_data/(?P<user>[-\w]+)/$', read.get_user, name='get user'),
    url(r'^account_profile/(?P<user>[-\w]+)/$', read.get_profile, name='get profile'),
    url(r'^account_card/(?P<user>[-\w]+)$', read.get_card, name='get card'),
    url(r'^thread_data/(?P<thread_id>\w+)/$', read.get_thread, name='get thread'),
    url(r'^civi_data/(?P<civi_id>\w+)$', read.get_civi, name='get civi'),
    url(r'^threads/(?P<thread_id>\w+)/civis$', read.get_civis, name='get civis'),
    url(r'^response_data/(?P<thread_id>\w+)/(?P<civi_id>\w+)/$', read.get_responses, name='get responses'),
    url(r'^feed/$', read.get_feed, name='get thread'),
    url(r'^new_thread/$', write.new_thread, name='new thread'),
    url(r'^edit_thread/$', write.editThread, name='edit thread'),
    url(r'^new_civi/$', write.createCivi, name='new civi'),
    url(r'^rate_civi/$', write.rateCivi, name='rate civi'),
    url(r'^edit_civi/$', write.editCivi, name='edit civi'),
    url(r'^delete_civi/$', write.deleteCivi, name='delete civi'),

    url(r'^invite/$',write.invite, name='invite users'),
    url(r'^edituser/$',write.editUser, name='edit user'),
    url(r'^upload_profile/$',write.uploadProfileImage, name='upload profile'),
    url(r'^upload_images/$',write.uploadCiviImage, name='upload images'),
    url(r'^upload_image/$',write.uploadThreadImage, name='upload image'),
    url(r'^clear_profile/$',write.clearProfileImage, name='clear profile'),
    url(r'^follow/$', write.requestFollow, name='follow user'),
    url(r'^unfollow/$', write.requestUnfollow, name='unfollow user'),
    url(r'^edit_user_categories/$', write.editUserCategories, name='edit user categories'),
]
