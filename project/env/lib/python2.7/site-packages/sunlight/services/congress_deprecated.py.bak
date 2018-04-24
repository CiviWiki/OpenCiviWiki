# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

"""
.. module:: sunlight.services.congress
    :synopsis: Sunlight Congress API Implementation

.. warning::
    Please avoid using this for new applications, this API has been
    phased out, and will be taken down at the end of the current
    congress.

Deprecated Sunlight Congress API Implementation inside ``python-sunlight``.
"""

import sunlight.service
import json

service_url = "http://services.sunlightlabs.com/api/"


def _unpack(resp, key):
    return [e[key] for e in resp[key + 's']]


class Congress(sunlight.service.Service):
    """
    Bindings into the `Sunlight Congress API
    <http://services.sunlightlabs.com/docs/Sunlight_Congress_API/>`_, an API
    primarily for details on current federal legislators.
    """

    def legislators(self, **kwargs):
        """
        Query for all legislators matching certain criteria.

        See documentation at `legislators.get(List)
        <http://services.sunlightlabs.com/docs/congressapi/legislators.get(List)/>`_
        """
        return _unpack(self.get('legislators.getList', **kwargs),
                       'legislator')

    def legislator_search(self, name, threshold=0.9, all_legislators=False,
                          **kwargs):
        """
        Fuzzy-matching name search against federal legislators.

        See documentation at `legislators.search
        <http://services.sunlightlabs.com/docs/congressapi/legislators.search/>`_
        """
        params = kwargs.copy()
        params.update({'name': name, 'threshold': threshold})

        if all_legislators:
            params['all_legislators'] = 1

        return _unpack(self.get('legislators.search', **params), 'result')

    def legislators_for_zip(self, zipcode, **kwargs):
        """
        Query for all legislators representing a given ZIP code.

        This method is not recommended, prefer legislators_for_lat_lon instead.
        See the blog post `"Don't Use Zip Codes Unless You Have To"
        <http://sunlightlabs.com/blog/2012/dont-use-zipcodes/>`_.

        See documentation at `legislators.allForZip
        <http://services.sunlightlabs.com/docs/congressapi/legislators.allForZip/>`_
        """
        params = kwargs.copy()
        params.update({
            "zip": zipcode
        })
        return _unpack(self.get('legislators.allForZip', **params),
                       'legislator')

    def legislators_for_lat_lon(self, latitude, longitude, **kwargs):
        """
        Query for all legislators representing an given location.

        See documentation at `legislators.allForLatLong
        <http://services.sunlightlabs.com/docs/congressapi/legislators.allForLatLong/>`_
        """
        params = kwargs.copy()
        params.update({
            "latitude": latitude,
            "longitude": longitude
        })
        return _unpack(self.get('legislators.allForLatLong', **params),
                       'legislator')

    def districts_for_zip(self, zipcode, **kwargs):
        """
        Query for all congressional districts overlapping a zip code.

        See documentation at `districts.getDistrictFromLatLong
        <http://services.sunlightlabs.com/docs/congressapi/districts.getDistrictFromLatLong/>`_
        """
        params = kwargs.copy()
        params.update({
            "zip": zipcode
        })
        return _unpack(self.get('districts.getDistrictsFromZip', **params),
                       'district')

    def districts_for_lat_lon(self, latitude, longitude, **kwargs):
        """
        Query for all congressional districts containing a given location.

        See documentation at `districts.getDistrictFromLatLong
        <http://services.sunlightlabs.com/docs/congressapi/districts.getDistrictFromLatLong/>`_
        """
        params = kwargs.copy()
        params.update({
            "latitude": latitude,
            "longitude": longitude
        })
        return _unpack(self.get('districts.getDistrictFromLatLong', **params),
                       'district')

    def committees(self, chamber, **kwargs):
        """
        Query for all committees for a chamber.  (House|Senate|Joint)

        See documentation at `committees.getList
        <http://services.sunlightlabs.com/docs/congressapi/committees.getList/>`_
        """
        params = kwargs.copy()
        params.update({"chamber": chamber})
        return _unpack(self.get('committees.getList', **params),
                       'committee')

    def committee_detail(self, committee_id, **kwargs):
        """
        Query for all details for a committee, including members.

        See documentation at `committees.get
        <http://services.sunlightlabs.com/docs/congressapi/committees.get/>`_
        """
        params = kwargs.copy()
        params.update({"id": committee_id})
        # We can't use _unpack since top level is `committee' not committees
        return self.get('committees.get', **params)['committee']

    def committees_for_legislator(self, bioguide_id, **kwargs):
        """
        Query for all details for all of a legislator's committee assignments.

        See documentation at `committees.allForLegislator
        <http://services.sunlightlabs.com/docs/congressapi/committees.allForLegislator/>`_
        """
        params = kwargs.copy()
        params.update({
            "bioguide_id": bioguide_id
        })
        return _unpack(self.get('committees.allForLegislator', **params),
                       'committee')

    # implementation methods
    def _get_url(self, obj, apikey, **kwargs):
        return "%s/%s?apikey=%s&%s" % (
            service_url,
            obj,
            apikey,
            sunlight.service.safe_encode(kwargs)
        )

    def _decode_response(self, response):
        return json.loads(response)['response']
