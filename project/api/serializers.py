from rest_framework import serializers

from api.forms import UpdateProfileImage
from api.models import Civi, Thread, Account, Category, CiviImage, Activity, Bill
from core.constants import CIVI_TYPES

WRITE_ONLY = {'write_only': True}


class AccountCommonSerializer(serializers.ModelSerializer):
    """ Common serializer for specific account serializers"""
    username = serializers.ReadOnlyField(source='user.username')
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        request = self.context.get("request")

        # Check for authenticated user
        if request and hasattr(request, "user") and request.user.is_authenticated:
            account = Account.objects.get(user=request.user)
            if obj in account.following.all():
                return True
        return False


class AccountSerializer(AccountCommonSerializer):
    """
    General seralizer for a single model instance of a user account
    """
    email = serializers.ReadOnlyField(source='user.email')

    profile_image = serializers.ImageField(write_only=True, allow_empty_file=False, required=False)
    profile_image_url = serializers.ReadOnlyField()
    profile_image_thumb_url = serializers.ReadOnlyField()

    address = serializers.CharField(allow_blank=True)
    zip_code = serializers.CharField(allow_blank=True)

    longitude = serializers.FloatField(max_value=180, min_value=-180, required=False)
    latitude = serializers.FloatField(max_value=90, min_value=-90, required=False)
    location = serializers.ReadOnlyField()

    is_staff = serializers.ReadOnlyField(source='user.is_staff')

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'about_me', 'location', 'email',
                  'address', 'city', 'state', 'zip_code', 'country', 'longitude', 'latitude',
                  'profile_image', 'profile_image_url', 'profile_image_thumb_url', 'is_staff',
                  'is_following')

        extra_kwargs = {
            'city': WRITE_ONLY,
            'state': WRITE_ONLY,
            'country': WRITE_ONLY,
        }

    def validate_profile_image(self, value):
        request = self.context['request']
        validation_form = UpdateProfileImage(request.POST, request.FILES)

        if validation_form.is_valid():
            # Clean up previous images
            account = Account.objects.get(user=request.user)
            account.profile_image.delete()
            account.profile_image_thumb.delete()

            return validation_form.clean_profile_image()
        else:
            raise serializers.ValidationError(validation_form.errors['profile_image'])


class AccountListSerializer(AccountCommonSerializer):
    """
    Seralizer for multiple account model instances
    """
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    location = serializers.ReadOnlyField()

    profile_image_url = serializers.ReadOnlyField()
    profile_image_thumb_url = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'profile_image_url',
                  'profile_image_thumb_url', 'location', 'is_following')


class CiviImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = CiviImage
        fields = ('id', 'civi', 'title', 'image_url', 'created')


class CiviSerializer(serializers.ModelSerializer):
    author = AccountListSerializer()
    type = serializers.ChoiceField(choices=CIVI_TYPES, source='c_type')
    images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    attachments = CiviImageSerializer(many=True, source='images')
    created = serializers.ReadOnlyField(source='created_date_str')
    score = serializers.SerializerMethodField()
    links = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="linked_civis")
    bills = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="linked_bills")

    class Meta:
        model = Civi
        fields = ('id', 'thread', 'type', 'title', 'body', 'author', 'created', 'last_modified',
                  'votes', 'images', 'linked_civis', 'links', 'responses', 'score', 'attachments', 'bills')

    def get_score(self, obj):
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
            account = Account.objects.get(user=user)
            return obj.score(account.id)


class CiviListSerializer(serializers.ModelSerializer):
    author = AccountListSerializer()
    type = serializers.CharField(source='c_type')
    created = serializers.ReadOnlyField(source='created_date_str')

    class Meta:
        model = Civi
        fields = ('id', 'thread', 'type', 'title', 'body', 'author', 'created')


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    preferred = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'preferred')

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

        account = Account.objects.get(user=user)
        return obj.id in account.categories.values_list('id', flat=True)


class ThreadSerializer(serializers.ModelSerializer):
    author = AccountListSerializer(required=False)
    category = CategoryListSerializer()

    civis = serializers.HyperlinkedRelatedField(many=True, view_name='civi-detail', read_only=True)
    created = serializers.ReadOnlyField(source='created_date_str')
    image = serializers.ImageField(write_only=True, allow_empty_file=False, required=False)

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = ('id', 'title', 'summary', 'author', 'image_url', 'civis', 'image',
                  'created', 'level', 'state', 'is_draft', 'category',
                  'num_views', 'num_civis', 'num_solutions')


class ThreadListSerializer(serializers.ModelSerializer):
    author = AccountListSerializer(required=False)
    category = CategoryListSerializer()

    created = serializers.ReadOnlyField()

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = ('id', 'title', 'summary', 'author', 'image_url', 'created',
                  'level', 'state', 'is_draft', 'category', 'num_views', 'num_civis',
                  'num_solutions')


class ThreadDetailSerializer(serializers.ModelSerializer):
    author = AccountListSerializer(required=False)
    category = CategoryListSerializer()

    civis = CiviSerializer(many=True)
    created = serializers.ReadOnlyField(source='created_date_str')
    image = serializers.ImageField(write_only=True, allow_empty_file=False, required=False)

    num_views = serializers.ReadOnlyField()
    num_civis = serializers.ReadOnlyField()
    num_solutions = serializers.ReadOnlyField()

    contributors = serializers.SerializerMethodField()
    user_votes = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ('id', 'title', 'summary', 'author', 'image_url', 'civis', 'image',
                  'created', 'level', 'state', 'is_draft', 'category',
                  'num_views', 'num_civis', 'num_solutions', 'contributors', 'user_votes')

    def get_contributors(self, obj):
        issue_civis = Civi.objects.filter(thread__id=obj.id)
        contributor_accounts = Account.objects.filter(
            pk__in=issue_civis.distinct('author').values_list('author', flat=True))
        return AccountListSerializer(contributor_accounts, many=True).data

    def get_user_votes(self, obj):
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user_activities = Activity.objects.filter(thread=obj.id, account=request.user.id)
            return [
                {'civi_id': activity.civi.id, 'activity_type': activity.activity_type, 'c_type': activity.civi.c_type}
                for activity in user_activities]
        else:
            return []


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"
