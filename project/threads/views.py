import json

from accounts.models import Profile
from accounts.utils import get_account
from categories.models import Category
from core.custom_decorators import full_profile, login_required
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from common.utils import check_database
from threads.models import Activity, Civi, CiviImage, Thread
from threads.permissions import IsOwnerOrReadOnly
from threads.serializers import (
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
        draft_threads = Thread.objects.filter(author=self.request.user, is_draft=True)
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


def base_view(request):
    if not request.user.is_authenticated:
        return TemplateResponse(request, "landing.html", {})

    Profile_filter = Profile.objects.get(user=request.user)
    if "login_user_image" not in request.session.keys():
        request.session["login_user_image"] = Profile_filter.profile_image_thumb_url

    categories = [{"id": c.id, "name": c.name} for c in Category.objects.all()]

    all_categories = list(Category.objects.values_list("id", flat=True))
    user_categories = (
        list(Profile_filter.categories.values_list("id", flat=True)) or all_categories
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
        for t in Thread.objects.filter(author_id=Profile_filter.id)
        .exclude(is_draft=False)
        .order_by("-created")
    ]

    data = {
        "categories": categories,
        "user_categories": user_categories,
        "threads": feed_threads,
        "trending": top5_threads,
        "draft_threads": my_draft_threads,
    }

    return TemplateResponse(request, "feed.html", {"data": json.dumps(data)})


@csrf_exempt
def civi2csv(request, thread_id):
    """
    CSV export function. Thread ID goes in, CSV HTTP response attachment goes out.
    """
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


is_sqlite_running = check_database("sqlite")


@login_required
@full_profile
def issue_thread(request, thread_id=None):
    if not thread_id:
        return HttpResponseRedirect("/404")

    Thread_filter = get_object_or_404(Thread, pk=thread_id)
    c_qs = Civi.objects.filter(thread_id=thread_id).exclude(c_type="response")
    c_scored = [c.dict_with_score(request.user.id) for c in c_qs]
    civis = sorted(c_scored, key=lambda c: c["score"], reverse=True)

    # modify thread view count
    Thread_filter.num_civis = len(civis)
    Thread_filter.num_views = F("num_views") + 1
    Thread_filter.save()
    Thread_filter.refresh_from_db()

    thread_wiki_data = {
        "thread_id": thread_id,
        "title": Thread_filter.title,
        "summary": Thread_filter.summary,
        "image": Thread_filter.image_url,
        "author": {
            "username": Thread_filter.author.username,
            "profile_image": Thread_filter.author.profile.profile_image_url,
            "first_name": Thread_filter.author.first_name,
            "last_name": Thread_filter.author.last_name,
        },
        "contributors": [
            Profile.objects.chip_summarize(p)
            for p in Profile.objects.filter(
                pk__in=c_qs.distinct("author").values_list("author", flat=True)
            )
        ]
        if not is_sqlite_running
        else [
            Profile.objects.chip_summarize(p)
            for p in Profile.objects.filter(
                pk__in=c_qs.values_list("author", flat=True).distinct()
            )
        ],
        "category": {
            "id": Thread_filter.category.id,
            "name": Thread_filter.category.name,
        },
        "categories": [{"id": c.id, "name": c.name} for c in Category.objects.all()],
        "created": Thread_filter.created_date_str,
        "num_civis": Thread_filter.num_civis,
        "num_views": Thread_filter.num_views,
        "user_votes": [
            {
                "civi_id": act.civi.id,
                "activity_type": act.activity_type,
                "c_type": act.civi.c_type,
            }
            for act in Activity.objects.filter(
                thread=Thread_filter.id, user=request.user.id
            )
        ],
    }
    thread_body_data = {
        "civis": civis,
    }

    data = {
        "thread_id": thread_id,
        "is_draft": Thread_filter.is_draft,
        "thread_wiki_data": json.dumps(thread_wiki_data),
        "thread_body_data": json.dumps(thread_body_data),
    }
    return TemplateResponse(request, "thread.html", data)


@login_required
@full_profile
def create_group(request):
    return TemplateResponse(request, "newgroup.html", {})


class DeclarationView(TemplateView):
    template_name = "declaration.html"


class LandingView(TemplateView):
    template_name = "landing.html"


class HowItWorksView(TemplateView):
    template_name = "how_it_works.html"


class AboutView(TemplateView):
    template_name = "about.html"


class SupportUsView(TemplateView):
    template_name = "support_us.html"
