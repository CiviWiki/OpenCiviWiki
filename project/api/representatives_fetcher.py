import requests
from django.conf import settings


class RepresentativesFetcherException(Exception):
    pass


class RepresentativesFetcher(object):
    URL = "https://projects.propublica.org/represent/location?q={}"

    def get_reps(self, address):
        url = self.URL.format(address)
        response = requests.get(url)
        if response.ok:
            return response.json()
        raise RepresentativesFetcherException("ProPublica API returned wrong response")
