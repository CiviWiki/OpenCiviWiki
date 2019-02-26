from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Civi, CiviImage
from api.serializers import CiviSerializer, CiviImageSerializer

from ..utils import get_account
from ..permissions import IsOwnerOrReadOnly


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
