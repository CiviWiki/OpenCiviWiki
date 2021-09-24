from rest_framework import serializers

from accounts.forms import UpdateProfileImage
from accounts.models import Profile

WRITE_ONLY = {"write_only": True}


class ProfileCommonSerializer(serializers.ModelSerializer):
    """ Common serializer for specific account serializers"""

    username = serializers.ReadOnlyField(source="user.username")
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        request = self.context.get("request")

        # Check for authenticated user
        if request and hasattr(request, "user") and request.user.is_authenticated:
            account = Profile.objects.get(user=request.user)
            if obj in account.following.all():
                return True
        return False


class ProfileSerializer(ProfileCommonSerializer):
    """
    General seralizer for a single model instance of a user account
    """

    email = serializers.ReadOnlyField(source="user.email")

    profile_image = serializers.ImageField(
        write_only=True, allow_empty_file=False, required=False
    )
    profile_image_url = serializers.ReadOnlyField()
    profile_image_thumb_url = serializers.ReadOnlyField()

    address = serializers.CharField(allow_blank=True)
    zip_code = serializers.CharField(allow_blank=True)

    longitude = serializers.FloatField(max_value=180, min_value=-180, required=False)
    latitude = serializers.FloatField(max_value=90, min_value=-90, required=False)
    location = serializers.ReadOnlyField()

    is_staff = serializers.ReadOnlyField(source="user.is_staff")

    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "about_me",
            "location",
            "email",
            "address",
            "city",
            "state",
            "zip_code",
            "country",
            "longitude",
            "latitude",
            "profile_image",
            "profile_image_url",
            "profile_image_thumb_url",
            "is_staff",
            "is_following",
        )

        extra_kwargs = {
            "city": WRITE_ONLY,
            "state": WRITE_ONLY,
            "country": WRITE_ONLY,
        }

    def validate_profile_image(self, value):
        """This function is used to validate the profile image before added to the user profile"""
        request = self.context["request"]
        validation_form = UpdateProfileImage(request.POST, request.FILES)

        if validation_form.is_valid():
            # Clean up previous images
            account = Profile.objects.get(user=request.user)
            account.profile_image.delete()
            account.profile_image_thumb.delete()

            return validation_form.clean_profile_image()
        else:
            raise serializers.ValidationError(validation_form.errors["profile_image"])


class ProfileListSerializer(ProfileCommonSerializer):
    """
    Serializer for multiple account model instances
    """

    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    location = serializers.ReadOnlyField()

    profile_image_url = serializers.ReadOnlyField()
    profile_image_thumb_url = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "profile_image_url",
            "profile_image_thumb_url",
            "location",
            "is_following",
        )
