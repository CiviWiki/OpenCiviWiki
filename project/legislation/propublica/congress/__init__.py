"""
A Python client for the ProPublica Congress API

API docs: https://propublica.github.io/congress-api-docs/

Most of my code has been either influenced by, or replaced by
code from Chris Amico's Propublica API code.
"""
import os

from .client import Client
from .utils import CongressError, NotFound, check_chamber, get_congress, CURRENT_CONGRESS

# subclients
from .bills import BillsClient
from .members import MembersClient
from .committees import CommitteesClient
from .votes import VotesClient
from .nominations import NominationsClient


__all__ = ('Congress', 'CongressError', 'NotFound', 'get_congress', 'CURRENT_CONGRESS')


class Congress(Client):
    """
    Everything returns decoded JSON, with fat trimmed.

    In addition, Chris made the top-level namespace a client, which
    can be used to fetch generic resources, using the API URIs included
    in responses.
    
    Congress uses httplib2, and caching is pluggable. By default,
    it uses `httplib2.FileCache, in a directory called .cache,
    but it should also work with memcache
    or anything else that exposes the same interface as FileCache.
    """

    def __init__(self, apikey=None, cache='.cache', http=None):
        if apikey is None:
            apikey = os.environ.get('PROPUBLICA_API_KEY')

        super(Congress, self).__init__(apikey, cache, http)

        self.bills = BillsClient(self.apikey, cache, self.http)
        self.committees = CommitteesClient(self.apikey, cache, self.http)
        self.members = MembersClient(self.apikey, cache, self.http)
        self.nominations = NominationsClient(self.apikey, cache, self.http)
        self.votes = VotesClient(self.apikey, cache, self.http)
