from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions import IsProfileOwnerOrDuringRegistrationOrReadOnly
from api.utils import get_account
from api.models import Thread
from accounts.models import Profile
from api.serializers import (
    ThreadSerializer,
    CategorySerializer,
    CiviSerializer,
    ProfileSerializer,
    ProfileListSerializer,
)


class ProfileViewSet(ModelViewSet):

    """
    REST API viewset for an Profile
    retrieve:
    Return the given user based a username.

    list:
    Return a list of all the existing users. Only with privileged access.
    """

    queryset = Profile.objects.all()
    lookup_field = "user__username"
    serializer_class = ProfileSerializer
    http_method_names = ["get", "head", "put", "patch"]
    permission_classes = (IsProfileOwnerOrDuringRegistrationOrReadOnly,)
    authentication_classes = ()

    def list(self, request):
        """ """
        if self.request.user.is_staff:
            accounts = Profile.objects.all()
        else:
            accounts = Profile.objects.filter(user=self.request.user)
        serializer = ProfileListSerializer(accounts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, user__username=None):
        """ """
        account = get_account(username=user__username)
        if self.request.user == account.user:
            serializer = ProfileSerializer(account)
        else:
            serializer = ProfileListSerializer(account)
        return Response(serializer.data)

    @action(detail=True)
    def civis(self, request, user__username=None):
        """
        Gets the civis of the selected account
        /accounts/{username}/civis
        """
        account = get_account(username=user__username)
        account_civis = account.civis
        serializer = CiviSerializer(account_civis, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def followers(self, request, user__username=None):
        """
        Gets the followers of the selected account
        /accounts/{username}/followers
        """
        account = get_account(username=user__username)
        account_followers = account.followers.all()
        serializer = ProfileListSerializer(account_followers, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def following(self, request, user__username=None):
        """
        Gets the followings of the selected account
        /accounts/{username}/following
        """
        account = get_account(username=user__username)
        account_followings = account.following.all()
        serializer = ProfileListSerializer(account_followings, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def categories(self, request, user__username=None):
        """
        Gets the preferred categories of the selected account
        /accounts/{username}/categories
        """
        account = get_account(username=user__username)
        account_categories = account.categories
        serializer = CategorySerializer(account_categories, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def threads(self, request, user__username=None):
        """
        Gets the preferred categories of the selected account
        /accounts/{username}/categories
        """
        account = get_account(username=user__username)
        draft_threads = Thread.objects.filter(author=account).exclude(is_draft=False)
        serializer = ThreadSerializer(
            draft_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def drafts(self, request, user__username=None):
        """
        Gets the draft threads of the selected account
        /accounts/{username}/drafts
        """
        account = get_account(username=user__username)
        draft_threads = Thread.objects.filter(author=account, is_draft=False)
        serializer = ThreadSerializer(
            draft_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)
