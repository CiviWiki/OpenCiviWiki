from rest_framework import serializers
from categories.models import Category
from accounts.models import Profile


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
