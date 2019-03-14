from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Thread, Account, Activity
from api.serializers import (
    ThreadSerializer,
    CategorySerializer,
    CiviSerializer,
    AccountSerializer,
    AccountListSerializer
)

from ..utils import get_account
from ..permissions import IsAccountOwnerOrDuringRegistrationOrReadOnly


class AccountViewSet(ModelViewSet):
    """
    REST API viewset for an Account
    retrieve:
    Return the given user based a username.

    list:
    Return a list of all the existing users. Only with privileged access.
    """

    queryset = Account.objects.all()
    lookup_field = 'user__username'
    serializer_class = AccountSerializer
    http_method_names = ['get', 'head', 'put', 'patch']
    permission_classes = (IsAccountOwnerOrDuringRegistrationOrReadOnly,)
    authentication_classes = ()

    def list(self, request):
        if self.request.user.is_staff:
            accounts = Account.objects.all()
        else:
            accounts = Account.objects.filter(user=self.request.user)
        serializer = AccountListSerializer(accounts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, user__username=None):
        account = get_account(username=user__username)
        if (self.request.user == account.user):
            serializer = AccountSerializer(account)
        else:
            serializer = AccountListSerializer(account)
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
        serializer = AccountListSerializer(account_followers, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def following(self, request, user__username=None):
        """
        Gets the followings of the selected account
        /accounts/{username}/following
        """
        account = get_account(username=user__username)
        account_followings = account.following.all()
        serializer = AccountListSerializer(account_followings, many=True)
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
        serializer = ThreadSerializer(draft_threads, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def drafts(self, request, user__username=None):
        """
        Gets the draft threads of the selected account
        /accounts/{username}/drafts
        """
        account = get_account(username=user__username)
        draft_threads = Thread.objects.filter(author=account, is_draft=False)
        serializer = ThreadSerializer(draft_threads, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def bills(self, request, user__username=None):
        """
        Gets the civis of the selected account
        /accounts/{username}/bills
        """
        account = get_account(username=user__username)
        activities = Activity.objects.filter(account=account)
        serializer = CiviSerializer(account_civis, many=True)
        return Response(serializer.data)