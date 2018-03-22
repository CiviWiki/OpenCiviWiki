from rest_framework import serializers
from api.models import Civi, Thread, Account, Category


WRITE_ONLY = {'write_only': True}

class AccountSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    profile_image_url = serializers.ReadOnlyField()
    profile_image_thumb_url = serializers.ReadOnlyField()

    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, coerce_to_string=False)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, coerce_to_string=False)
    location = serializers.ReadOnlyField()
    civis = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'about_me', 'location',
        'address', 'city', 'state', 'zip_code', 'longitude', 'latitude',
        'profile_image', 'profile_image_url', 'profile_image_thumb_url',
        'civis')

        # NOTE: Not sure if write only should be indicated above like read only
        extra_kwargs = {
            'profile_image': WRITE_ONLY,
            'address': WRITE_ONLY,
            'city': WRITE_ONLY,
            'state': WRITE_ONLY,
            'zip_code': WRITE_ONLY,
            'longitude': WRITE_ONLY,
            'latitude': WRITE_ONLY,
        }

    def validate_longitude(self, value):
        """
        Check that the blog post is about Django.
        """
        try:
            long = float(value)
        except ValueError:
            raise serializers.ValidationError("Longitude value cannot be converted")

        if long > 180 or long < -180:
            raise serializers.ValidationError("Invalid Longitude Value")
        return long

    def validate_latitude(self, value):
        """
        Check that the blog post is about Django.
        """
        try:
            lat = float(value)
        except ValueError:
            raise serializers.ValidationError("Latitude value cannot be converted")

        if lat > 90 or lat < -90:
            raise serializers.ValidationError("Invalid Latitude Value")
        return lat



class CiviSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.full_name') #TODO: more detailed
    type = serializers.CharField(source='c_type')

    class Meta:
        model = Civi
        fields = ('id', 'type', 'title', 'body')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ThreadSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.full_name') #TODO: more detailed
    civis = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'title', 'summary', 'author', 'category_id', 'image_url', 'civis')
