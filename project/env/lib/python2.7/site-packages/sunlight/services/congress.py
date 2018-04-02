# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

"""
.. module:: sunlight.services.congress
    :synopsis: Sunlight Congress API Implementation

Sunlight Congress API Implementation inside ``python-sunlight``.
"""

import sunlight.service
from sunlight.service import EntityDict, EntityList
from sunlight.pagination import pageable
from sunlight.errors import SunlightException
import json


API_DOMAIN = "congress.api.sunlightfoundation.com"

LEGISLATOR_ID_TYPES = (
    'bioguide',
    'ocd',
    'thomas',
    'lis',
    'govtrack',
    'votesmart',
    'crp',
    'fec',
)


# Stolen from http://codereview.stackexchange.com/a/21035/28391
def flatten_dict(d):
    def flat_items():
        for k, v in list(d.items()):
            if isinstance(v, dict):
                for kk, vv in list(flatten_dict(v).items()):
                    yield '{0}.{1}'.format(k, kk), vv
            else:
                yield k, v

    return dict(flat_items())


def preencode_values(d):
    for k, v in list(d.items()):
        if isinstance(v, bool):
            d[k] = str(v).lower()
    return d


class Congress(sunlight.service.Service):
    """
    Bindings to the `Congress API <http://sunlightlabs.github.io/congress/>`_.
    Keep in mind this is a thin wrapper around the API so the API documentation
    is the place to look for help on field names and examples.

    By default, the API runs over https. You can set `congress.use_https = False` or
    `congress = Congress(use_https=False)` to use regular http.
    """

    is_pageable = True

    def __init__(self, use_https=True):
        super(Congress, self).__init__()
        self._selected_protocol = 'https'
        self.use_https = use_https

    @property
    def use_https(self):
        """
            This API supports https and regular http. Default is to use https
        """
        return self._use_https

    @use_https.setter
    def use_https(self, value):
        self._use_https = value
        if self._use_https:
            self._selected_protocol = 'https'
        else:
            self._selected_protocol = 'http'

    @pageable
    def legislators(self, **kwargs):
        """
        Search and filter for members of Congress.

        For details see `Legislators API docs
        <http://sunlightlabs.github.io/congress/legislators.html>`
        """
        return self.get(['legislators'], **kwargs)

    @pageable
    def legislator(self, identifier, id_type=LEGISLATOR_ID_TYPES[0], **kwargs):
        """
        Retrieve a member of Congress by a unique identifier. Defaults to
        bioguide. Choices are:

            * bioguide
            * ocd
            * thomas
            * lis
            * govtrack
            * votesmart
            * crp
            * fec

        For details see `Legislators API docs
        <http://sunlightlabs.github.io/congress/legislators.html>`
        """
        if id_type not in LEGISLATOR_ID_TYPES:
            id_type = LEGISLATOR_ID_TYPES[0]
        id_arg = {}
        if id_type == 'fec':
            id_arg['fec_ids'] = identifier
        else:
            id_key = '{0}_id'.format(id_type)
            id_arg[id_key] = '"{0}"'.format(identifier)

        kwargs.update(id_arg)
        results = self.get(['legislators'], **kwargs)
        if results and len(results):
            return EntityDict(results[0], results._meta)
        return None

    def all_legislators_in_office(self, **kwargs):
        """
        Returns all legislators currently in office (non-paginated response).

        For details see `Legislators API docs
        <http://sunlightlabs.github.io/congress/legislators.html>`_
        """
        kwargs.update({
            "per_page": "all"
        })
        return self.get(['legislators'], **kwargs)

    @pageable
    def locate_legislators_by_lat_lon(self, lat, lon, **kwargs):
        """
        Find members of Congress by a latitude and longitude.

        For details see `Legislators API docs
        <http://sunlightlabs.github.io/congress/legislators.html#methods/legislators-locate>`_
        """
        kwargs.update({
            "latitude": lat,
            "longitude": lon
        })
        return self.get(['legislators', 'locate'], **kwargs)

    @pageable
    def locate_legislators_by_zip(self, zipcode, **kwargs):
        """
        Find members of Congress by zip code.

        For details see `Legislators API docs
        <http://sunlightlabs.github.io/congress/legislators.html#methods/legislators-locate>`_
        """
        kwargs.update({
            "zip": zipcode
        })
        return self.get(['legislators', 'locate'], **kwargs)

    @pageable
    def bills(self, **kwargs):
        """
        Search and filter through bills in Congress.

        For details see `Bills API docs
        <http://sunlightlabs.github.io/congress/bills.html>`_
        """
        return self.get(['bills'], **kwargs)

    @pageable
    def bill(self, bill_id, **kwargs):
        """
        Retrieve a bill by bill_id.

        For details see `Bills API docs
        <http://sunlightlabs.github.io/congress/bills.html>`_
        """
        kwargs.update({
            "bill_id": bill_id
        })
        results = self.get(['bills'], **kwargs)
        if results and len(results):
            return EntityDict(results[0], results._meta)
        return None

    @pageable
    def search_bills(self, query, **kwargs):
        """
        Search the full text of legislation, and other fields.

        For details see `Bill search API docs
        <http://sunlightlabs.github.io/congress/bills.html#methods/bills-search>`_
        """
        kwargs.update({
            "query": query
        })
        return self.get(['bills', 'search'], **kwargs)

    @pageable
    def upcoming_bills(self, **kwargs):
        """
        Search and filter through upcoming bills in the House and Senate.

        This will return bills that have been scheduled by
        party leadership for upcoming House and Senate floor action.

        For details see `Upcoming Bills API docs
        <http://sunlightlabs.github.io/congress/upcoming_bills.html>`_
        """
        return self.get(['upcoming_bills'], **kwargs)

    @pageable
    def locate_districts_by_lat_lon(self, lat, lon, **kwargs):
        """
        Find congressional districts by a latitude and longitude.

        For details see `Districts API docs
        <http://sunlightlabs.github.io/congress/districts.html>`_
        """
        kwargs.update({
            "latitude": lat,
            "longitude": lon
        })
        return self.get(['districts', 'locate'], **kwargs)

    @pageable
    def locate_districts_by_zip(self, zipcode, **kwargs):
        """
        Find congressional districts by a latitude and longitude.

        For details see `Districts API docs
        <http://sunlightlabs.github.io/congress/districts.html>`_
        """
        kwargs.update({
            "zip": zipcode,
        })
        return self.get(['districts', 'locate'], **kwargs)

    @pageable
    def committees(self, **kwargs):
        """
        Search and filter through committees in the House and Senate.

        For details see `Committees API docs
        <http://sunlightlabs.github.io/congress/committees.html>`_
        """
        return self.get(['committees'], **kwargs)

    @pageable
    def amendments(self, **kwargs):
        """
        Search and filter through amendments in Congress.

        For details see `Amendments API docs
        <http://sunlightlabs.github.io/congress/amendments.html>`_
        """
        return self.get(['amendments'], **kwargs)

    @pageable
    def votes(self, **kwargs):
        """
        Search and filter through votes in Congress.

        For details see `Votes API docs
        <http://sunlightlabs.github.io/congress/votes.html>`_
        """
        return self.get(['votes'], **kwargs)

    @pageable
    def floor_updates(self, **kwargs):
        """
        Search and filter through floor updates in the House and Senate.

        For details see `Floor Updates API docs
        <http://sunlightlabs.github.io/congress/floor_updates.html>`_
        """
        return self.get(['floor_updates'], **kwargs)

    @pageable
    def hearings(self, **kwargs):
        """
        Search and filter through committee hearings in the House and Senate.

        For details see `Hearings API docs
        <http://sunlightlabs.github.io/congress/hearings.html>`_
        """
        return self.get(['hearings'], **kwargs)

    @pageable
    def nominations(self, **kwargs):
        """
        Search and filter through presidential nominations in Congress.

        For details see `Nominations API docs
        <http://sunlightlabs.github.io/congress/nominations.html>`_
        """
        return self.get(['nominations'], **kwargs)

    @pageable
    def congressional_documents(self, **kwargs):
        """
        Search congressional documents including House witness documents and
        House committee reports.

        For details see `Congressional documents API docs
        <https://sunlightlabs.github.io/congress/congressional_documents.html>`_
        """
        return self.get(['congressional_documents', 'search'], **kwargs)

    @pageable
    def documents(self, **kwargs):
        """
        Search oversight documents including Government Accountability Office reports and
        Inspectors General reports.

        For details see `Documents API docs
        <https://sunlightlabs.github.io/congress/documents.html>`_
        """
        return self.get(['documents'], **kwargs)

    # implementation methods
    def _get_url(self, pathparts, apikey, **kwargs):
        url_args = preencode_values(flatten_dict(kwargs))

        # join pieces by slashes and add a trailing slash
        endpoint_path = "/".join(pathparts)

        url = "{api_protocol}://{api_domain}/{path}?apikey={apikey}&{url_args}".format(
            api_protocol=self._selected_protocol,
            api_domain=API_DOMAIN,
            path=endpoint_path,
            apikey=apikey,
            url_args=sunlight.service.safe_encode(url_args)
        ).strip('&')
        return url

    def _decode_response(self, response):
        try:
            data = json.loads(response)
        except Exception:
            raise SunlightException('Error parsing response! Something must be wrong with our Congress... API')
        results = data.pop('results', None)
        if results:
            return EntityList(results, data)
        else:
            return None
