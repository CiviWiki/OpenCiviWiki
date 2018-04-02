# -*- coding: utf-8 -*-

"""A Python client for the Open States API"""

from __future__ import unicode_literals, print_function, absolute_import
import os
from sys import version_info
from datetime import datetime
from requests import Session

"""Copyright 2016 Sean Whalen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

__version__ = "1.1.0"

API_ROOT = "https://openstates.org/api/v1/"
DEFAULT_USER_AGENT = "pyopenstates/{0}".format(__version__)
ENVIRON_API_KEY = os.environ.get('OPENSTATES_API_KEY')

session = Session()
session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
if ENVIRON_API_KEY:
    session.headers.update({'X-Api-Key': ENVIRON_API_KEY})

#  Python 2 comparability hack
if version_info[0] >= 3:
    unicode = str


class APIError(RuntimeError):
    """
    Raised when the Open States API returns an error
    """
    pass


class NotFound(APIError):
    """Raised when the API cannot find the requested object"""
    pass


def _get(uri, params=None):
    """
    An internal method for making API calls and error handling easy and consistent
    Args:
        uri: API URI
        params: GET parameters

    Returns:
        JSON as a Python dictionary
    """

    def _convert_timestamps(result):
        """Converts a string timestamps from an api result API to a datetime"""
        if type(result) == dict:
            for key in result.keys():
                if type(result[key]) == unicode:
                    try:
                        result[key] = datetime.strptime(result[key],
                                                        "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            result[key] = datetime.strptime(result[key],
                                                            "%Y-%m-%d")
                        except ValueError:
                            pass
                elif type(result[key]) == dict:
                    result[key] = _convert_timestamps(result[key])
                elif type(result) == list:
                    result = list(map(lambda r: _convert_timestamps(r), result))
        elif type(result) == list:
            result = list(map(lambda r: _convert_timestamps(r), result))

        return result

    def _convert(result):
        """Convert results to standard Python data structures"""
        result = _convert_timestamps(result)

        return result

    url = "{0}/{1}/".format(API_ROOT.strip("/"), uri.strip("/"))
    for param in params.keys():
        if type(params[param]) == list:
            params[param] = ",".join(params[param])
    response = session.get(url, params=params)
    if response.status_code != 200:
        if response.status_code == 404:
            raise NotFound("Not found: {0}".format(response.url))
        else:
            raise APIError(response.text)
    return _convert(response.json())


def set_user_agent(user_agent):
    """Appends a custom string to the default User-Agent string
    (e.g. ``pyopenstates/__version__ user_agent``)"""
    session.headers.update({"User-Agent": "{0} {1}".format(DEFAULT_USER_AGENT,
                                                           user_agent)})


def set_api_key(apikey):
    """Sets API key. Can also be set as OPENSTATES_API_KEY environment
    variable."""
    session.headers['X-Api-Key'] = apikey


def get_metadata(state=None, fields=None):
    """
        Returns a list of all states with data available, and basic metadata about their status. Can also get detailed
        metadata for a particular state.

    Args:
        state: The abbreviation of state to get detailed metadata on, or leave as None to get high-level metadata on all
        states.

        fields: An optional list of fields to return; returns all fields by default

    Returns:
       Dict: The requested :ref:`Metadata` as a dictionary

    """
    uri = "/metadata/"
    if state:
        uri += "{0}/".format(state.lower())
    return _get(uri, params=dict(fields=fields))


def download_bulk_data(state, file_object, data_format="json"):
    """
    Downloads a zip containing bulk data on a given state to a given file object

    Args:
        state: The abbreviation of the state
        file_object: A file or file-like object
        data_format: ``json`` or ``csv``

    .. NOTE::
        ``json`` format provides much more detail than ``csv``.

    Examples:
        ::

            # Saving Ohio's data to a file on disk
            with open("ohio-json.zip", "wb") as ohio_zip_file:
                pyopenstates.bulk_download("OH", ohio_zip_file)

            # Or download it to memory
            from io import BytesIO
            mem_zip = BytesIO()
            pyopenstates.bulk_download("OH", mem_zip)

    """
    if data_format.lower() == "json":
        field = "latest_json_url"
    elif data_format.lower() == "csv":
        field = "latest_csv_url"
    else:
        raise ValueError("data_format must be json or csv")
    url = get_metadata(state, fields=field)[field]
    response = session.get(url)
    if response.status_code != 200:
        if response.status_code == 404:
            raise NotFound("Not found: {0}".format(response.url))
        else:
            raise APIError(response.text)

    file_object.write(response.content)


def search_bills(**kwargs):
    """
    Find bills matching a given set of filters

    Args:
        **kwargs: One or more search filters

    - ``state`` - Only return bills from a given state (e.g. ``nc``)
    - ``chamber`` - Only return bills matching the provided chamber (``upper`` or ``lower``)
    - ``bill_id`` - Only return bills with a given bill_id.
    - ``bill_id_in`` - Accepts a pipe (|) delimited list of bill ids.
    - ``q`` -  Only return bills matching the provided full text query.
    - ``search_window``- By default all bills are searched, but if a time window is desired the following options can be
        passed to ``search_window``:
        - ``search_window=all`` - Default, include all sessions.
        - ``search_window=term`` - Only bills from sessions within the current term.
        - ``search_window=session`` - Only bills from the current session.
        - ``search_window=session:2009`` - Only bills from the session named ``2009``.
        - ``search_window=term:2009-2011`` - Only bills from the sessions in the ``2009-2011`` session.
    - ``updated_since`` - Only bills updated since a provided date (provided in ``YYYY-MM-DD`` format)
    - ``sponsor_id`` Only bills sponsored by a given legislator id (e.g. ``ILL000555``)
    - ``subject`` - Only bills categorized by Open States as belonging to this subject.
    - ``type`` Only bills of a given type (e.g. ``bill``, ``resolution``, etc.)

    You can specify sorting using the following ``sort`` keyword argument values:

    - ``first``
    - ``last``
    - ``signed``
    - ``passed_lower``
    - ``passed_upper``
    - ``updated_at``
    - ``created_at``

    Returns:
        A list of matching :ref:`Bill` dictionaries

    .. NOTE::
        This method returns just a subset (``state``, ``chamber``, ``session``,
        ``subjects``, ``type``, ``id``, ``bill_id``, ``title``, ``created_at``,
        ``updated_at``) of the bill fields by default.

        Use the ``fields`` parameter to specify a custom list of fields to return.
    """
    uri = "bills/"
    if "per_page" in kwargs.keys():
        results = []
        kwargs["page"] = 1
        new_results = _get(uri, params=kwargs)
        while len(new_results) > 0:
            results += new_results
            kwargs["page"] += 1
            new_results = _get(uri, params=kwargs)
    else:
        results = _get(uri, params=kwargs)

    return results


def get_bill(uid=None, state=None, term=None, bill_id=None, **kwargs):
    """
    Returns details of a specific bill Can be identified my the Open States unique bill id (uid), or by specifying
    the state, term, and legislative bill ID

    Args:
        uid: The Open States unique bill ID
        state: The postal code of the state
        term: The legislative term (see state metadata)
        bill_id: Yhe legislative bill ID (e.g. ``HR 42``)
        **kwargs: Optional keyword argument options, such as ``fields``, which specifies the fields to return

    Returns:
        The :ref:`Bill` details as a dictionary
    """
    if uid:
        if state or term or bill_id:
            raise ValueError("Must specify an Open States bill (uid), or the state, term, and bill ID")
        return _get("/bills/{}".format(uid), params=kwargs)
    else:
        if not state or not term or not bill_id:
            raise ValueError("Must specify an Open States bill (uid), or the state, term, and bill ID")
        return _get("/bills/{}/{}/{}/".format(state.lower(), term, bill_id), params=kwargs)


def search_legislators(**kwargs):
    """
    Search for legislators

    Args:
        **kwargs: One or more search filters

    - ``state`` - Filter by state.
    - ``first_name`` -  Filter by first name.
    - ``last_name`` - Filter by last name.
    - ``chamber`` - Only legislators with a role in the specified chamber.
    - ``active`` - ``True`` (default) to only include current legislators, ``False`` will include all legislators
    - ``term`` - Only legislators that have a role in a certain term.
    - ``district`` - Only legislators that have represented the specified district.
    - ``party`` - Only legislators that have been associated with a specified party.

    Returns:
        A list of matching :ref:`Legislator` dictionaries

    """
    return _get("/legislators/", params=kwargs)


def get_legislator(leg_id, fields=None):
    """
    Gets a legislator's details

    Args:
        leg_id: The Legislator's Open States ID
        fields: An optional custom list of fields to return

    Returns:
        The requested :ref:`Legislator` details as a dictionary
    """
    return _get("/legislators/{0}/".format(leg_id), params=dict(fields=fields))


def locate_legislators(lat, long, fields=None):
    """
    Returns a list of legislators for the given latitude/longitude coordinates

    Args:
        lat: Latitude
        long: Longitude
        fields: An optional custom list of fields to return

    Returns:
        A list of matching :ref:`Legislator` dictionaries

    """
    return _get("/legislators/geo/", params=dict(lat=lat, long=long, fields=fields))


def search_committees(**kwargs):
    """
    Search for and return a list of matching committees

    Args:
        **kwargs: One or more filter keyword arguments

    - ``committee`` - Name of committee.
    - ``subcommittee`` - Name of subcommittee. (if None, object describes the committee)
    - ``chamber`` - Chamber committee belongs to: ``upper``, ``lower``, or ``joint``
    - ``state`` - State abbreviation

    Returns:
        A list of matching :ref:`Committee` dictionaries
    """
    return _get("/committees/", params=kwargs)


def get_committee(com_id, fields=None):
    """
    Gets committee details

    Args:
        com_id: Open States committee ID
        fields: An optional, custom set of fields to return

    Returns:
        The requested :ref:`Committee` details as a dictionary
    """
    return _get("/committees/{0}/".format(com_id), params=dict(fields=fields))


def search_events(**kwargs):
    """
    Searches events

    Events are not available in all states, to ensure that events are available check the ``feature_flags`` list in a
    states’ State Metadata.

    Args:
        **kwargs: One or more search filters

    - ``state`` - State abbreviation.
    - ``type`` - Categorized event type. (``committee:meeting`` for now)

    This method also allows specifying an alternate output format, by specifying ``format=rss`` or ``format=ics``.

    Returns:
        A list of matching :ref:`Event` dictionaries
    """
    return _get("/events/", params=kwargs)


def get_event(event_id, fields=None):
    """
    Gets event details

    Args:
        event_id: The Open States Event UUID
        fields: An optional list of fields to return

    Returns:
        The requested :ref:`Event` details as a dictionary
    """
    return _get("/events/{0}/".format(event_id), params=dict(fields=fields))


def search_districts(state, chamber, fields=None):
    """
    Search for districts

    Args:
        state: The state to search in
        chamber: the upper or lower legislative chamber
        fields: Optionally specify a custom list of fields to return

    Returns:
       A list of matching :ref:`District` dictionaries
    """
    uri = "/districts/{}/".format(state.lower())
    if chamber:
        chamber = chamber.lower()
        uri += "{}/".format(chamber)
        if chamber not in ["upper", "lower"]:
            raise ValueError('Chamber must be "upper" or "lower"')
        return _get(uri, params=dict(fields=fields))


def get_district(boundary_id, fields=None):
    """
    Gets district details

    Args:
        boundary_id: The boundary ID
        fields: Optionally specify a custom list of fields to return

    Returns:
        The requested :ref:`District` details as a dictionary
    """
    uri = "/districts/boundary/{0}/".format(boundary_id)
    return _get(uri, params=dict(fields=fields))
