"""
RESTful API View Definitions

"""
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import (
    api_view,
    detail_route,
)
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import Thread, Account, Category, Civi, CiviImage
from api.serializers import (
    ThreadSerializer,
    CategorySerializer,
    CiviSerializer,
    CiviImageSerializer,
    AccountSerializer,
    AccountListSerializer
)


# API Root view ==========================================/
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('category-list', request=request, format=format),
        'threads': reverse('thread-list', request=request, format=format),
        'accounts': reverse('account-list', request=request, format=format),
        'civis': reverse('civi-list', request=request, format=format),
    })

# Instance Access Helper Functions =======================/
def get_account(user=None, pk=None, username=None):
    """ gets author based on the user """
    if user:
        return get_object_or_404(Account, user=user)
    elif pk:
        return get_object_or_404(Account, pk=pk)
    elif username:
        return get_object_or_404(Account, user__username=username)

    else:
        raise Http404


# Custom Authentication/Permission Classes ================/
class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Custom API permission to check if request user is the owner of the model """

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS) or
            (obj.author == get_account(user=request.user))
        )
class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """ Custom API permission to check if request user is the owner of the account """

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS) or
            (obj.user == request.user)
        )


# Bypass CSRF Session conflict in DRF
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


AUTH_CLASSES = (authentication.BasicAuthentication)
if settings.DEBUG:
    AUTH_CLASSES = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)


# Viewset Definitions =====================================/
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ REST API viewset for Categories """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @detail_route()
    def threads(self, request, pk=None):
        category_threads = Thread.objects.filter_by_category_id(pk)
        serializer = ThreadSerializer(category_threads, many=True)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
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
    permission_classes = (IsAccountOwnerOrReadOnly,)

    def list(self, request):
        if self.request.user.is_staff:
            accounts = Account.objects.all()
        else:
            accounts = Account.objects.filter(user=self.request.user)
        serializer = AccountListSerializer(accounts, many=True)
        return Response(serializer.data)

    @detail_route()
    def civis(self, request, user__username=None):
        """
        Gets the civis of the selected account
        /accounts/{username}/civis
        """
        account = get_account(username=user__username)
        account_civis = account.civis
        serializer = CiviSerializer(account_civis, many=True)
        return Response(serializer.data)

    @detail_route()
    def followers(self, request, user__username=None):
        """
        Gets the followers of the selected account
        /accounts/{username}/followers
        """
        account = get_account(username=user__username)
        account_followers = account.followers.all()
        serializer = AccountListSerializer(account_followers, many=True)
        return Response(serializer.data)

    @detail_route()
    def following(self, request, user__username=None):
        """
        Gets the followings of the selected account
        /accounts/{username}/following
        """
        account = get_account(username=user__username)
        account_followings = account.following.all()
        serializer = AccountListSerializer(account_followings, many=True)
        return Response(serializer.data)

    @detail_route()
    def categories(self, request, user__username=None):
        """
        Gets the preferred categories of the selected account
        /accounts/{username}/categories
        """
        account = get_account(username=user__username)
        account_categories = account.categories
        serializer = CategorySerializer(account_categories, many=True)
        return Response(serializer.data)

class ThreadViewSet(viewsets.ModelViewSet):
    """ REST API viewset for Threads """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = AUTH_CLASSES

    def perform_create(self, serializer):
        serializer.save(author=get_account(user=self.request.user))

    @detail_route()
    def civis(self, request, pk=None):
        """
        Gets the civis linked to the thread instance
        /accounts/{username}/civis
        """
        thread_civis = Civi.objects.filter_by_thread_id(pk)
        serializer = CiviSerializer(thread_civis, many=True)
        return Response(serializer.data)

class CiviViewSet(viewsets.ModelViewSet):
    """ REST API viewset for Civis """

    queryset = Civi.objects.all()
    serializer_class = CiviSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = AUTH_CLASSES

    def perform_create(self, serializer):
        serializer.save(author=get_account(user=self.request.user))

    @detail_route()
    def images(self, request, pk=None):
        """
        Gets the related images
        /accounts/{username}/images
        """
        civi_images = CiviImage.objects.filter(civi=pk)
        serializer = CiviImageSerializer(civi_images, many=True, read_only=True)
        return Response(serializer.data)
