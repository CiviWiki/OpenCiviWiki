import json

from accounts.forms import ProfileEditForm, UpdateProfileImage
from accounts.models import Profile
from accounts.utils import get_account
from categories.models import Category
from core.constants import US_STATES
from core.custom_decorators import full_profile, login_required
from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from threads.models import Activity, Civi, Thread

from .models import Civi, CiviImage, Thread
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CiviImageSerializer,
    CiviSerializer,
    ThreadDetailSerializer,
    ThreadListSerializer,
    ThreadSerializer,
)


class ThreadViewSet(ModelViewSet):
    queryset = Thread.objects.order_by("-created")
    serializer_class = ThreadDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def list(self, request):
        threads = Thread.objects.filter(is_draft=False).order_by("-created")
        serializer = ThreadSerializer(threads, many=True, context={"request": request})
        return Response(serializer.data)

    def get_queryset(self):
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


class CiviViewSet(ModelViewSet):
    """REST API viewset for Civis"""

    queryset = Civi.objects.all()
    serializer_class = CiviSerializer
    permission_classes = (IsOwnerOrReadOnly,)

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


class CategoryViewSet(ReadOnlyModelViewSet):
    """REST API viewset for Categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = ()

    @action(detail=True)
    def threads(self, request, pk=None):
        category_threads = Thread.objects.filter_by_category_id(pk)
        serializer = ThreadSerializer(category_threads, many=True)
        return Response(serializer.data)


def base_view(request):
    if not request.user.is_authenticated:
        return TemplateResponse(request, "static_templates/landing.html", {})

    profile_filter = Profile.objects.get(user=request.user)
    if "login_user_image" not in request.session.keys():
        request.session["login_user_image"] = profile_filter.profile_image_thumb_url

    categories = [{"id": c.id, "name": c.name} for c in Category.objects.all()]

    all_categories = list(Category.objects.values_list("id", flat=True))
    user_categories = (
        list(profile_filter.categories.values_list("id", flat=True)) or all_categories
    )

    feed_threads = [
        Thread.objects.summarize(t)
        for t in Thread.objects.exclude(is_draft=True).order_by("-created")
    ]
    top5_threads = list(
        Thread.objects.filter(is_draft=False)
        .order_by("-num_views")[:5]
        .values("id", "title")
    )
    my_draft_threads = [
        Thread.objects.summarize(t)
        for t in Thread.objects.filter(author_id=profile_filter.id)
        .exclude(is_draft=False)
        .order_by("-created")
    ]

    states = sorted(US_STATES, key=lambda s: s[1])
    data = {
        "categories": categories,
        "states": states,
        "user_categories": user_categories,
        "threads": feed_threads,
        "trending": top5_threads,
        "draft_threads": my_draft_threads,
    }

    return TemplateResponse(request, "feed.html", {"data": json.dumps(data)})


@login_required
@full_profile
def issue_thread(request, thread_id=None):
    if not thread_id:
        return HttpResponseRedirect("/404")

    req_acct = Profile.objects.get(user=request.user)
    thread_filter = Thread.objects.get(id=thread_id)
    c_qs = Civi.objects.filter(thread_id=thread_id).exclude(c_type="response")
    c_scored = [c.dict_with_score(req_acct.id) for c in c_qs]
    civis = sorted(c_scored, key=lambda c: c["score"], reverse=True)

    # modify thread view count
    thread_filter.num_civis = len(civis)
    thread_filter.num_views = F("num_views") + 1
    thread_filter.save()
    thread_filter.refresh_from_db()

    thread_wiki_data = {
        "thread_id": thread_id,
        "title": thread_filter.title,
        "summary": thread_filter.summary,
        "image": thread_filter.image_url,
        "author": {
            "username": thread_filter.author.user.username,
            "profile_image": thread_filter.author.profile_image_url,
            "first_name": thread_filter.author.first_name,
            "last_name": thread_filter.author.last_name,
        },
        "contributors": [
            Profile.objects.chip_summarize(a)
            for a in Profile.objects.filter(
                pk__in=civis.distinct("author").values_list("author", flat=True)
            )
        ],
        "category": {
            "id": thread_filter.category.id,
            "name": thread_filter.category.name,
        },
        "categories": [{"id": c.id, "name": c.name} for c in Category.objects.all()],
        "states": sorted(US_STATES, key=lambda s: s[1]),
        "created": thread_filter.created_date_str,
        "level": thread_filter.level,
        "state": thread_filter.state if thread_filter.level == "state" else "",
        "location": thread_filter.level
        if not thread_filter.state
        else dict(US_STATES).get(thread_filter.state),
        "num_civis": thread_filter.num_civis,
        "num_views": thread_filter.num_views,
        "user_votes": [
            {
                "civi_id": act.civi.id,
                "activity_type": act.activity_type,
                "c_type": act.civi.c_type,
            }
            for act in Activity.objects.filter(
                thread=thread_filter.id, account=req_acct.id
            )
        ],
    }
    thread_body_data = {
        "civis": civis,
    }

    data = {
        "thread_id": thread_id,
        "is_draft": thread_filter.is_draft,
        "thread_wiki_data": json.dumps(thread_wiki_data),
        "thread_body_data": json.dumps(thread_body_data),
    }
    return TemplateResponse(request, "thread.html", data)


@csrf_exempt
def civi2csv(request, thread_id):
    import csv

    thread = thread_id
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=" + thread + ".csv"
    writer = csv.writer(response, delimiter=",")
    for card in Civi.objects.filter(thread_id=thread):
        data = []
        for key, value in card.dict_with_score().items():
            if value:
                data.append(value)
        writer.writerow(data)
    return response
