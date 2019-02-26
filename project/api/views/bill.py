from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Bill
from api.serializers import BillSerializer
from api.propublica import ProPublicaAPI


class BillViewSet(ModelViewSet):
    """ REST API viewset for Bills """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=False)
    def search(self, request):
        """
        Gets the all found bills
        /bills/search?query=<query>
        """
        query = request.get('query')
        if not query:
            return Response(status=400)

        found_bills = ProPublicaAPI().search(query)
        bills_to_serialize = []
        for found_bill in found_bills:
            bill, _ = Bill.objects.get_or_create(id=found_bill['bill_id'])
            bill.update(found_bill)
            bills_to_serialize.append(bill)

        serializer = self.get_serializer(bills_to_serialize, many=True)
        return Response(serializer.data)
