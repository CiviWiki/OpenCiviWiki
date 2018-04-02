# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

import sunlight.service
from sunlight.errors import BadRequestException
import json

module_name = "openstates"
service_url = "http://openstates.org/api/v1"


class Openstates(sunlight.service.Service):
    """
    Bindings into the `Open States API <http://openstates.org/api/>`_. Keep in
    mind this is a thin wrapper around the API so the API documentation is the
    place to look for help on field names and examples.
    """

    def all_metadata(self, **kwargs):
        """
        Get an overview of all available states including each state's name
        and abbreviation.

        For details see
        `Metadata Overview <http://openstates.org/api/metadata/#metadata-overview>`_.
        """
        return self.get(["metadata"], **kwargs)

    def state_metadata(self, state, **kwargs):
        """
        Complete metadata for a given state, containing information on
        the particulars of this state's chambers, sessions, and terms.

        For details see
        `State Metadata <http://openstates.org/api/metadata/#state-metadata>`_.
        """
        return self.get(["metadata", state], **kwargs)

    def bills(self, **kwargs):
        """
        Search the entirety of bills available via the Open States API.

        The fields and keyword arguments can be found on the
        `Bill API docs <http://openstates.org/api/bills/>`_.
        """
        return self.get(["bills"], **kwargs)

    def bill(self, bill_id, **kwargs):
        """
        Get full information on a single bill from the Open States API given
        the OpenStates Bill ID (such as TNB00004685)

        `Bill API docs <http://openstates.org/api/bills/>`_.
        """
        return self.get(["bills", bill_id], **kwargs)

    def bill_detail(self, state, session, bill_id, chamber=None):
        """
        Get full information on a single bill from the Open States API given
        a ``state``, ``session``, and ``bill_id`` (and optionally ``chamber``
        if the request would be ambiguous without one).

        The fields and keyword arguments can be found on the
        `Open States Bill API docs <http://openstates.org/api/bills/>`_.
        """
        lss = ["bills", state, str(session)]
        if chamber:
            lss.append(chamber)
        lss.append(bill_id)
        return self.get(lss)

    def legislators(self, **kwargs):
        """
        Search the entirety of legislators available via the Open States API.

        The fields and keyword arguments can be found on the
        `Legislator API docs <http://openstates.org/api/legislators/>`_.
        """
        return self.get(["legislators"], **kwargs)

    def legislator_detail(self, leg_id, **kwargs):
        """
        Get detailed information on a single legislator given their Open States
        Legislator ID.

        The ``leg_id`` argument is a legislator ID code used throughout the
        Open States API, such as ``MDL000210``.

        For details on fields see the `Legislator API Fields
        <http://openstates.org/api/legislators/#legislator-fields>`_.
        """
        return self.get(["legislators", leg_id], **kwargs)

    def legislator_geo_search(self, latitude, longitude, **kwargs):
        """
        Given a latitude and longitude return all legislators that represent
        districts containing that point.

        See the Open States documentation for examples of `Legislator Geo
        Lookup <http://openstates.org/api/legislators/#geo-lookup>`_.
        """
        kwargs['lat'] = latitude
        kwargs['long'] = longitude
        return self.get(["legislators", "geo"], **kwargs)

    def committees(self, **kwargs):
        """
        Search against all committees available via the Open States API.

        Committee fields and keyword arguments can be found on the
        `Committee API docs <http://openstates.org/api/committees/>`_.
        """
        return self.get(["committees"], **kwargs)

    def committee_detail(self, committee_id, **kwargs):
        """
        Get detailed information on a single committee given its Open States
        Committee ID.

        The ``committee_id`` argument is a committee ID code used throughout
        the Open States API, such as ``MDC000065``.

        For details on fields see the `Committee API Fields
        <http://openstates.org/api/committees/#committee-fields>`_.
        """
        return self.get(["committees", committee_id], **kwargs)

    def events(self, **kwargs):
        """
        Query the Open States API for information regarding upcoming events
        taken from a state-level legislative calendar.

        See the Open States' site for details on the
        `Event API <http://openstates.org/api/events/>`_.
        """
        return self.get(["events"], **kwargs)

    def event_detail(self, event_id, **kwargs):
        """
        Get detailed informaton regarding a single event.

        ``event_id`` is an OpenStates event ID, such as ``TXE00000990``.

        See the Open States' site for details on the
        `Event API Fields <http://openstates.org/api/events/#event-fields>`_.
        """
        lss = ["events", event_id]
        return self.get(lss, **kwargs)

    def districts(self, state, chamber=None, **kwargs):
        """
        Get a listing of districts for a state (optionally narrowed by
        chamber).

        For a listing of fields see `District Fields
        <http://openstates.org/api/districts/#district-fields>`_.
        """
        pieces = ['districts', state]
        if chamber:
            pieces.append(chamber)
        return self.get(pieces, **kwargs)

    def district_boundary(self, boundary_id, **kwargs):
        """
        Get a detailed GeoJSON-style boundary for a given district given a
        boundary_id (available via the :meth:``districts``.

        ``boundary_id`` resembles ``sldl-tx-state-house-district-35``.

        For a listing of fields see `District Fields
        <http://openstates.org/api/districts/#district-fields>`_.

        For more information on this method and example output see
        `District Boundary Lookup
        <http://openstates.org/api/districts/#district-boundary-lookup>`_
        """
        return self.get(['districts', 'boundary', boundary_id], **kwargs)

    # API impl methods

    def _get_url(self, objs, apikey, **kwargs):
        # Gate for any None's in the query. This is usually a problem.
        if None in objs:
            raise BadRequestException("`None' passed to the URL encoder (%s)" %
                                      (str(objs)))

        # join pieces by slashes and add a trailing slash
        object_path = "/".join(objs)
        object_path += "/"

        return "%s/%s?apikey=%s&%s" % (
            service_url,
            object_path,
            apikey,
            sunlight.service.safe_encode(kwargs)
        )

    def _decode_response(self, response):
        return json.loads(response)
