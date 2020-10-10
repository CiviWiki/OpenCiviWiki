from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Thread, Civi
from api.serializers import (
    ThreadSerializer,
    ThreadListSerializer,
    ThreadDetailSerializer,
    CiviSerializer,
)

from ..utils import get_account
from ..permissions import IsOwnerOrReadOnly


class ThreadViewSet(ModelViewSet):
    """ REST API viewset for Threads """

    queryset = Thread.objects.order_by("-created")
    serializer_class = ThreadDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def list(self, request):
        threads = Thread.objects.filter(is_draft=False).order_by("-created")
        serializer = ThreadSerializer(threads, many=True, context={"request": request})
        return Response(serializer.data)

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = Thread.objects.all()
        category_id = self.request.query_params.get("category_id", None)
        if category_id is not None:
            if category_id != "all":
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

    @action(methods=["get", "post"], detail=False)
    def all(self, request):
        """
        Gets the all threads for listing
        /threads/all
        """
        all_threads = self.queryset
        serializer = ThreadListSerializer(
            all_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(methods=["get", "post"], detail=False)
    def top(self, request):
        """
        Gets the top threads based on the number of page views
        /threads/top
        """
        limit = request.query_params.get("limit", 5)
        top_threads = Thread.objects.filter(is_draft=False).order_by("-num_views")[
            :limit
        ]
        serializer = ThreadListSerializer(
            top_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False)
    def drafts(self, request):
        """
        Gets the drafts of the current authenticated user
        /threads/drafts
        """
        account = get_account(username=self.request.user)
        draft_threads = Thread.objects.filter(author=account, is_draft=True)
        serializer = ThreadListSerializer(
            draft_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)
