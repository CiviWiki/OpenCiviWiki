from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Bill
from api.serializers import BillSerializer


class BillViewSet(ModelViewSet):
    """ REST API viewset for Bills """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
