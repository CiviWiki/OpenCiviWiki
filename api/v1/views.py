from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from django.conf import settings

@api_view(['GET'])
def open_states_api_endpoint(request):
    if request.method == 'GET':
        # Create a request to fake data API
        api_response = requests.get("https://reqres.in/api/users/2")

        return Response(api_response)
