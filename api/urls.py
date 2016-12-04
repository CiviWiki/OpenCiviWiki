from django.conf.urls import url
import read, write

urlpatterns = [
    # url(r'^getcivi$', read.getCivi, name='civi'),
    # url(r'^topten$', read.topTen, name='example'),
    # url(r'^topics$', read.getTopics, name='get topics'),
    # url(r'^categories$', read.getCategories, name='get categories'),
    # url(r'^useridbyusername$', read.getIdByUsername, name='get id by username'),
    url(r'^account_data/(?P<user>\w+)/$', read.getUser, name='get user'),
    url(r'^account_profile/(?P<user>\w+)/$', read.getProfile, name='get profile'),
    url(r'^thread_data/(?P<thread_id>\w+)/$', read.getThread, name='get thread'),
    # url(r'^getblock$', read.getBlock, name='get block'),
    # url(r'^creategroup$', write.createGroup, name='add group'),
    # url(r'^createcivi$', write.createCivi, name='add civi'),
    url(r'^edituser/$',write.editUser, name='edit user'),
    url(r'^upload_profile/$',write.uploadProfileImage, name='upload profile'),
    url(r'^clear_profile/$',write.clearProfileImage, name='clear profile'),
    # url(r'^requestfriend$',write.requestFriend, name='request friend'),
    # url(r'^acceptfriend$',write.acceptFriend, name='accept friend'),
    # url(r'^removefriend$',write.removeFriend, name='remove friend'),
    # url(r'^followgroup$',write.followGroup, name='follow group'),
    # url(r'^unfollowgroup$', write.unfollowGroup, name='unfollow group'),
    # url(r'^pincivi$', write.pinCivi, name='pin civi'),
    # url(r'^unpincivi$', write.unpinCivi, name='unpin civi')
]
