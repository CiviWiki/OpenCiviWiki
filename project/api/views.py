"""
RESTful API View Definitions

"""

from django.http import Http404
from django.shortcuts import get_object_or_404
# from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    detail_route,
    list_route
)
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


from api.models import Thread, Account, Category, Civi
from api.serializers import (
    ThreadSerializer,
    CategorySerializer,
    CiviSerializer,
    AccountSerializer
)



# API Root view
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('category-list', request=request, format=format),
        'threads': reverse('thread-list', request=request, format=format),
        'accounts': reverse('account-list', request=request, format=format)
    })

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


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Custom API permission to check if request user is the owner of the model """

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS) or
            (obj.author == get_account(user=request.user))
        )
class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """ Custom API permission to check if request user is the owner of the model """

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS) or
            (obj.user == request.user)
        )

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ RESTful API viewset for Categories """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @detail_route()
    def threads(self, request, pk=None):
        category_threads = Thread.objects.filter_by_category_id(pk)
        serializer = ThreadSerializer(category_threads, many=True)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    """ RESTful API viewset for a Account """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get', 'head', 'put', 'patch']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAccountOwnerOrReadOnly,)

    @list_route(url_path='username/(?P<username>\w+)')
    def get_by_username(self, request, username):
        """
        Gets a user account by username
        /accounts/username/{username}
        """
        account = get_account(username=username)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    @detail_route()
    def civis(self, request, pk=None):
        """
        Gets the civis of the selected account
        /accounts/{pk}/civis
        """
        account = get_account(pk=pk)
        account_civis = account.civis
        serializer = CiviSerializer(account_civis, many=True)
        return Response(serializer.data)

    @detail_route()
    def followers(self, request, pk=None):
        """
        Gets the followers of the selected account
        /accounts/{pk}/followers
        """
        account = get_account(pk=pk)
        account_followers = account.followers.all()
        serializer = AccountSerializer(account_followers, many=True)
        return Response(serializer.data)

    @detail_route()
    def following(self, request, pk=None):
        """
        Gets the followings of the selected account
        /accounts/{pk}/following
        """
        account = get_account(pk=pk)
        account_followings = account.following.all()
        serializer = AccountSerializer(account_followings, many=True)
        return Response(serializer.data)


class ThreadViewSet(viewsets.ModelViewSet):
    """ RESTful API viewset for Threads """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        """ allows us to modify how the instance save is managed """
        serializer.save(author=get_account(user=self.request.user))

    @detail_route()
    def civis(self, request, pk=None):
        thread_civis = Civi.objects.filter_by_thread_id(pk)
        serializer = CiviSerializer(thread_civis, many=True)
        return Response(serializer.data)
