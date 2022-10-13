import json

from accounts.models import Profile
from accounts.utils import get_account
from categories.models import Category
from core.custom_decorators import full_profile, login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from threads.models import Civi, CiviImage, Thread
from threads.permissions import IsOwnerOrReadOnly
from threads.serializers import (
    CiviImageSerializer,
    CiviSerializer,
    ThreadDetailSerializer,
    ThreadListSerializer,
    ThreadSerializer,
)


class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    context_object_name = "thread"
    template_name = "thread.html"
    login_url = "accounts_login"

    def get_context_data(self, **kwargs):
        context = super(ThreadDetailView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["problems"] = Civi.objects.problems(thread_id=context["thread"].id)
        context["causes"] = Civi.objects.causes(thread_id=context["thread"].id)
        context["solutions"] = Civi.objects.solutions(thread_id=context["thread"].id)
        return context


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
        for _key, value in card.dict_with_score().items():
            if value:
                data.append(value)
        writer.writerow(data)
    return response


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
