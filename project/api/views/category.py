from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Thread
<<<<<<< HEAD
from categories.models import Category
=======
>>>>>>> f693e3c878920b2ff58c282b4f88f507b61bf985
from api.serializers import ThreadSerializer, CategorySerializer
from categories.models import Category


class CategoryViewSet(ReadOnlyModelViewSet):
    """ REST API viewset for Categories """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = ()

    @action(detail=True)
    def threads(self, request, pk=None):
        category_threads = Thread.objects.filter_by_category_id(pk)
        serializer = ThreadSerializer(category_threads, many=True)
        return Response(serializer.data)
