from django.conf.urls import url
import read, write

from api.v1.views import open_states_bills

#TODO: RESTful API - http://www.django-rest-framework.org/
urlpatterns = [
    # url(r'^getcivi$', read.getCivi, name='civi'),
    # url(r'^topten$', read.topTen, name='example'),
    # url(r'^topics$', read.getTopics, name='get topics'),
    # url(r'^categories$', read.getCategories, name='get categories'),
    # url(r'^useridbyusername$', read.getIdByUsername, name='get id by username'),

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

    # url(r'^getblock$', read.getBlock, name='get block'),
    # url(r'^creategroup$', write.createGroup, name='add group'),
    # url(r'^createcivi$', write.createCivi, name='add civi'),
    url(r'^invite/$',write.invite, name='invite users'),
    url(r'^edituser/$',write.editUser, name='edit user'),
    url(r'^upload_profile/$',write.uploadProfileImage, name='upload profile'),
    url(r'^upload_images/$',write.uploadCiviImage, name='upload images'),
    url(r'^upload_image/$',write.uploadThreadImage, name='upload image'),
    url(r'^clear_profile/$',write.clearProfileImage, name='clear profile'),
    url(r'^follow/$', write.requestFollow, name='follow user'),
    url(r'^unfollow/$', write.requestUnfollow, name='unfollow user'),
    url(r'^edit_user_categories/$', write.editUserCategories, name='edit user categories'),


    # url(r'^requestfriend$',write.requestFriend, name='request friend'),
    # url(r'^acceptfriend$',write.acceptFriend, name='accept friend'),
    # url(r'^removefriend$',write.removeFriend, name='remove friend'),
    # url(r'^followgroup$',write.followGroup, name='follow group'),
    # url(r'^unfollowgroup$', write.unfollowGroup, name='unfollow group'),
    # url(r'^pincivi$', write.pinCivi, name='pin civi'),
    # url(r'^unpincivi$', write.unpinCivi, name='unpin civi'),

    # api
    url(r'^v1/open_states/bills/$', open_states_bills),
]
