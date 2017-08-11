from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import pyopenstates as open_states

from django.conf import settings

@api_view(['GET'])
def open_states_api_endpoint(request):
    if request.method == 'GET':
        # Get OpenStates API key
        open_states_api_key = settings.OPEN_STATES_API_KEY

        # Initialize OpenStates with API key
        open_states.set_api_key(open_states_api_key)

        # Get query parameter from request, False if not provided
        query = request.GET.get('query', False)

        if (query):
            # Get some data from OpenStates API
            api_response = open_states.search_bills(q=query)

            return Response(api_response)
