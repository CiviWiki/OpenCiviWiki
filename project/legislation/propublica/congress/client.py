"""
Base client outlining how we fetch and parse responses
"""
import json
import logging
import httplib2

from .utils import NotFound, CongressError, u

log = logging.getLogger('congress')


class Client(object):
    """
    Client classes deal with fetching responses from the ProPublica Congress
    API and parsing what comes back. In addition to storing API credentials,
    a client can use a custom cache, or even a customized
    httplib2.Http instance.
    """

    BASE_URI = "https://api.propublica.org/congress/v1/"

    def __init__(self, apikey=None, cache='.cache', http=None):
        self.apikey = apikey

        if isinstance(http, httplib2.Http):
            self.http = http
        else:
            self.http = httplib2.Http(cache)

    def fetch(self, path, parse=lambda r: r['results'][0]):
        """
        Make an API request, with authentication.

        This method can be used directly to fetch new endpoints
        or customize parsing.

        ::

            >>> from congress import Congress
            >>> client = Congress()
            >>> senate = client.fetch('115/senate/members.json')
            >>> print(senate['num_results'])
            101

        """
        url = self.BASE_URI + path
        headers = {'X-API-Key': self.apikey}

        log.debug(url)

        resp, content = self.http.request(url, headers=headers)
        content = u(content)
        content = json.loads(content)

        # handle errors
        if not content.get('status') == 'OK':

            if "errors" in content and content['errors'][0]['error'] == "Record not found":
                raise NotFound(path)

            if content.get('status') == '404':
                raise NotFound(path)

            raise CongressError(content, resp, url)

        if callable(parse):
            content = parse(content)

        return content
