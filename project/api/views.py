"""
RESTful API View Definitions

"""
<<<<<<< HEAD

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
=======
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import (
    api_view,
    action
)
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import Thread, Account, Category, Civi, CiviImage
from api.serializers import (
    ThreadSerializer,
    ThreadListSerializer,
    ThreadDetailSerializer,
    CategorySerializer,
    CiviSerializer,
    CiviImageSerializer,
    AccountSerializer,
    AccountListSerializer
)


# API Root view ==========================================/
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('category-list', request=request, format=format),
        'threads': reverse('thread-list', request=request, format=format),
<<<<<<< HEAD
        'accounts': reverse('account-list', request=request, format=format)
    })

=======
        'accounts': reverse('account-list', request=request, format=format),
        'civis': reverse('civi-list', request=request, format=format),
    })

# Instance Access Helper Functions =======================/
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6
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


<<<<<<< HEAD
=======
# Custom Authentication/Permission Classes ================/
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6
class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Custom API permission to check if request user is the owner of the model """

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS) or
            (obj.author == get_account(user=request.user))
        )
class IsAccountOwnerOrReadOnly(permissions.BasePermission):
<<<<<<< HEAD
    """ Custom API permission to check if request user is the owner of the model """
=======
    """ Custom API permission to check if request user is the owner of the account """
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS) or
            (obj.user == request.user)
        )

<<<<<<< HEAD
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ RESTful API viewset for Categories """
=======

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
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

<<<<<<< HEAD
    @detail_route()
=======
    @action(detail=True)
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6
    def threads(self, request, pk=None):
        category_threads = Thread.objects.filter_by_category_id(pk)
        serializer = ThreadSerializer(category_threads, many=True)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
<<<<<<< HEAD
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
=======
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
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6
        account_civis = account.civis
        serializer = CiviSerializer(account_civis, many=True)
        return Response(serializer.data)

<<<<<<< HEAD
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
=======
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

class ThreadViewSet(viewsets.ModelViewSet):
    """ REST API viewset for Threads """

    queryset = Thread.objects.order_by('-created')
    serializer_class = ThreadDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = AUTH_CLASSES

    def list(self, request):
        threads = Thread.objects.filter(is_draft=False).order_by('-created')
        serializer = ThreadSerializer(threads, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = Thread.objects.all()
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            if category_id != 'all':
                queryset = queryset.filter(category=category_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=get_account(user=self.request.user))

    @action(detail=True)
    def civis(self, request, pk=None):
        """
        Gets the civis linked to the thread instance
        /threads/{id}/civis
        """
        thread_civis = Civi.objects.filter(thread=pk)
        serializer = CiviSerializer(thread_civis, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=False)
    def all(self, request):
        """
        Gets the all threads for listing
        /threads/all
        """
        all_threads = self.queryset
        serializer = ThreadListSerializer(all_threads, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=False)
    def top(self, request):
        """
        Gets the top threads based on the number of page views
        /threads/top
        """
        limit = request.query_params.get('limit', 5)
        top_threads = Thread.objects.filter(is_draft=False).order_by('-num_views')[:limit]
        serializer = ThreadListSerializer(top_threads, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def drafts(self, request):
        """
        Gets the drafts of the current authenticated user
        /threads/drafts
        """
        account = get_account(username=self.request.user)
        draft_threads = Thread.objects.filter(author=account, is_draft=True)
        serializer = ThreadListSerializer(draft_threads, many=True, context={'request': request})
        return Response(serializer.data)

class CiviViewSet(viewsets.ModelViewSet):
    """ REST API viewset for Civis """

    queryset = Civi.objects.all()
    serializer_class = CiviSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = AUTH_CLASSES

    def perform_create(self, serializer):
        serializer.save(author=get_account(user=self.request.user))

    @action(detail=True)
    def images(self, request, pk=None):
        """
        Gets the related images
        /civis/{id}/images
        """
        civi_images = CiviImage.objects.filter(civi=pk)
        serializer = CiviImageSerializer(civi_images, many=True, read_only=True)
        return Response(serializer.data)
>>>>>>> f5feb83f8f912194e913b0931668541112143eb6
