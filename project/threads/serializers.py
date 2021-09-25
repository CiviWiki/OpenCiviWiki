from accounts.models import Profile
from accounts.serializers import ProfileListSerializer
from core.constants import CIVI_TYPES
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .forms import UpdateProfileImage
from .models import Activity, Category, Civi, CiviImage, Thread
from .permissions import IsOwnerOrReadOnly
from .utils import get_account

WRITE_ONLY = {"write_only": True}


class CategoryListSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = Category
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    """ """
    preferred = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "preferred")

    def get_preferred(self, obj):
        user = None
        request = self.context.get("request")

        # Check for authenticated user
        if request and hasattr(request, "user"):
            user = request.user
        else:
            return True

        if user.is_anonymous():
            return True

        account = Profile.objects.get(user=user)
        return obj.id in account.categories.values_list("id", flat=True)


class CiviImageSerializer(serializers.ModelSerializer):
    """ """
    image_url = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = CiviImage
        fields = ("id", "civi", "title", "image_url", "created")


class CiviImageSerializer(serializers.ModelSerializer):
    """ """
    image_url = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = CiviImage
        fields = ("id", "civi", "title", "image_url", "created")

class ThreadSerializer(serializers.ModelSerializer):

    author = ProfileListSerializer(required=False)
    category = CategoryListSerializer()

    civis = serializers.HyperlinkedRelatedField(
        many=True, view_name="civi-detail", read_only=True
    )
    created = serializers.ReadOnlyField(source="created_date_str")
    image = serializers.ImageField(
        write_only=True, allow_empty_file=False, required=False
    )

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "image_url",
            "civis",
            "image",
            "created",
            "level",
            "state",
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
        )


class ThreadListSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer(required=False)
    category = CategoryListSerializer()

    created = serializers.ReadOnlyField()

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "image_url",
            "created",
            "level",
            "state",
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
        )

class CiviSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer()
    type = serializers.ChoiceField(choices=CIVI_TYPES, source="c_type")
    images = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="image_url"
    )
    attachments = CiviImageSerializer(many=True, source="images")
    created = serializers.ReadOnlyField(source="created_date_str")
    score = serializers.SerializerMethodField()
    links = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source="linked_civis"
    )

    class Meta:
        model = Civi
        fields = (
            "id",
            "thread",
            "type",
            "title",
            "body",
            "author",
            "created",
            "last_modified",
            "votes",
            "images",
            "linked_civis",
            "links",
            "responses",
            "score",
            "attachments",
        )

    def get_score(self, obj):
        """ """
        user = None
        request = self.context.get("request")

        # Check for authenticated user
        if request and hasattr(request, "user"):
            user = request.user
        else:
            return 0

        if user.is_anonymous():
            return 0
        else:
            account = Profile.objects.get(user=user)
            return obj.score(account.id)


class CiviListSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer()
    type = serializers.CharField(source="c_type")
    created = serializers.ReadOnlyField(source="created_date_str")

    class Meta:
        model = Civi
        fields = ("id", "thread", "type", "title", "body", "author", "created")


class ThreadDetailSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer(required=False)
    category = CategoryListSerializer()

    civis = CiviSerializer(many=True)
    created = serializers.ReadOnlyField(source="created_date_str")
    image = serializers.ImageField(
        write_only=True, allow_empty_file=False, required=False
    )

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    contributors = serializers.SerializerMethodField()
    user_votes = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "image_url",
            "civis",
            "image",
            "created",
            "level",
            "state",
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
            "contributors",
            "user_votes",
        )

    def get_contributors(self, obj):
        """This function gets the list of contributors for Civiwiki"""
        issue_civis = Civi.objects.filter(thread__id=obj.id)
        contributor_accounts = Profile.objects.filter(
            pk__in=issue_civis.values("author").distinct()
        )
        return ProfileListSerializer(contributor_accounts, many=True).data

    def get_user_votes(self, obj):
        """This function gets the user votes"""
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user_activities = Activity.objects.filter(
                thread=obj.id, account=request.user.id
            )
            return [
                {
                    "civi_id": activity.civi.id,
                    "activity_type": activity.activity_type,
                    "c_type": activity.civi.c_type,
                }
                for activity in user_activities
            ]
        else:
            return []


class ThreadSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer(required=False)
    category = CategoryListSerializer()

    civis = serializers.HyperlinkedRelatedField(
        many=True, view_name="civi-detail", read_only=True
    )
    created = serializers.ReadOnlyField(source="created_date_str")
    image = serializers.ImageField(
        write_only=True, allow_empty_file=False, required=False
    )

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "image_url",
            "civis",
            "image",
            "created",
            "level",
            "state",
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
        )


class ThreadListSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer(required=False)
    category = CategoryListSerializer()

    created = serializers.ReadOnlyField()

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "image_url",
            "created",
            "level",
            "state",
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
        )


class ThreadDetailSerializer(serializers.ModelSerializer):
    """ """
    author = ProfileListSerializer(required=False)
    category = CategoryListSerializer()

    civis = CiviSerializer(many=True)
    created = serializers.ReadOnlyField(source="created_date_str")
    image = serializers.ImageField(
        write_only=True, allow_empty_file=False, required=False
    )

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    contributors = serializers.SerializerMethodField()
    user_votes = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "image_url",
            "civis",
            "image",
            "created",
            "level",
            "state",
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
            "contributors",
            "user_votes",
        )

    def get_contributors(self, obj):
        """This function gets the list of contributors for Civiwiki"""
        issue_civis = Civi.objects.filter(thread__id=obj.id)
        contributor_accounts = Profile.objects.filter(
            pk__in=issue_civis.values("author").distinct()
        )
        return ProfileListSerializer(contributor_accounts, many=True).data

    def get_user_votes(self, obj):
        """This function gets the user votes"""
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user_activities = Activity.objects.filter(
                thread=obj.id, account=request.user.id
            )
            return [
                {
                    "civi_id": activity.civi.id,
                    "activity_type": activity.activity_type,
                    "c_type": activity.civi.c_type,
                }
                for activity in user_activities
            ]
        else:
            return []

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

class CiviViewSet(ModelViewSet):
    """ REST API viewset for Civis """

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
