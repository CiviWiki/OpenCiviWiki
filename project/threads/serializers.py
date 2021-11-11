from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Civi, Thread, CiviImage, Activity
from accounts.serializers import UserListSerializer
from categories.serializers import CategoryListSerializer
from core.constants import CIVI_TYPES

WRITE_ONLY = {"write_only": True}


class CiviImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = CiviImage
        fields = ("id", "civi", "title", "image_url", "created")


class CiviSerializer(serializers.ModelSerializer):
    author = UserListSerializer()
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

        if not user.is_authenticated:
            return 0
        else:
            return obj.score(user.id)


class CiviListSerializer(serializers.ModelSerializer):
    """ """

    author = UserListSerializer()
    type = serializers.CharField(source="c_type")
    created = serializers.ReadOnlyField(source="created_date_str")

    class Meta:
        model = Civi
        fields = ("id", "thread", "type", "title", "body", "author", "created")


class ThreadSerializer(serializers.ModelSerializer):
    """ """

    author = UserListSerializer(required=False)
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
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
        )


class ThreadListSerializer(serializers.ModelSerializer):
    """ """

    author = UserListSerializer(required=False)
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
            "is_draft",
            "category",
            "num_views",
            "num_civis",
            "num_solutions",
        )


class ThreadDetailSerializer(serializers.ModelSerializer):
    """ """

    author = UserListSerializer(required=False)
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
        contributor_users = get_user_model().objects.filter(
            pk__in=issue_civis.values("author").distinct()
        )
        return UserListSerializer(contributor_users, many=True).data

    def get_user_votes(self, obj):
        """This function gets the user votes"""
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user_activities = Activity.objects.filter(
                thread=obj.id, user=request.user.id
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
