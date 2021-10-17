from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.forms import UpdateProfileImage
from accounts.models import Profile


class ProfileCommonSerializer(serializers.ModelSerializer):
    """Common serializer for specific profile serializers"""

    username = serializers.ReadOnlyField(source="user.username")
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        request = self.context.get("request")

        # Check for authenticated user
        if request and hasattr(request, "user") and request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            if obj in profile.following.all():
                return True
        return False


class ProfileSerializer(ProfileCommonSerializer):
    """
    General serializer for a single model instance of a user profile
    """

    email = serializers.ReadOnlyField(source="user.email")

    profile_image = serializers.ImageField(
        write_only=True, allow_empty_file=False, required=False
    )
    profile_image_url = serializers.ReadOnlyField()
    profile_image_thumb_url = serializers.ReadOnlyField()

    is_staff = serializers.ReadOnlyField(source="user.is_staff")

    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "about_me",
            "email",
            "profile_image",
            "profile_image_url",
            "profile_image_thumb_url",
            "is_staff",
            "is_following",
        )

    def validate_profile_image(self, value):
        """
        This function is used to validate
        the profile image before added to the user profile
        """
        request = self.context["request"]
        validation_form = UpdateProfileImage(request.POST, request.FILES)

        if validation_form.is_valid():
            # Clean up previous images
            profile = Profile.objects.get(user=request.user)
            profile.profile_image.delete()
            profile.profile_image_thumb.delete()

            return validation_form.clean_profile_image()
        else:
            raise serializers.ValidationError(validation_form.errors["profile_image"])


class ProfileListSerializer(ProfileCommonSerializer):
    """
    Serializer for multiple profile model instances
    """

    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

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
            "is_following",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    General serializer for a single model instance of a user
    """

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        )
        read_only_fields = ("username", "email", "is_staff")


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for multiple user model instances
    """

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username", "first_name", "last_name")
