import requests
from django.conf import settings


class ProPublicaAPI(object):
    URL = 'https://api.propublica.org/congress/v1/bills/search.json?query="{query}"'

    def __init__(self, api_key=None):
        self.api_key = api_key or settings.PROPUBLICA_API_KEY
        self.auth_headers = {'X-API-Key': self.api_key}

    def search(self, query):
        if not self.api_key:
            return {}
        response = requests.get(self.URL.format(query=query), headers=self.auth_headers)
        response.raise_for_status()
        return response.json()
