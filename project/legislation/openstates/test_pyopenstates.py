#!/usr/bn/env python
# -*- coding: utf-8 -*-

"""Unit tests for openstatesclient"""

import unittest

from io import BytesIO
from zipfile import ZipFile
from datetime import datetime
from time import sleep
import pyopenstates

"""Copyright 2016 Sean Whalen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Test(unittest.TestCase):
    """A test suite for pyopenstates"""

    def setUp(self):
        pyopenstates.set_user_agent("test-suite")

    def tearDown(self):
        # Wait between tests to avoid hitting the API limit
        sleep(0.5)

    def testOpenStatesMetadata(self):
        """Calling the metadata method without specifying a state returns a
        list of 52 dictionaries: One for each state, plus DC and Puerto Rico"""
        metadata = pyopenstates.get_metadata()
        self.assertEqual(len(metadata), 52)
        for obj in metadata:
            self.assertEqual(type(obj), dict)

    def testStateMetadata(self):
        """All default state metadata fields are returned"""
        state_code = "NC"
        fields = ['name', 'latest_csv_url', 'latest_csv_date', 'chambers',
                  'capitol_timezone', 'id', 'latest_json_url',
                  'session_details', 'terms','latest_json_date',
                  'latest_update', 'abbreviation', 'legislature_name',
                  'feature_flags', 'legislature_url']
        metadata = pyopenstates.get_metadata(state_code)
        keys = metadata.keys()
        for field in fields:
            self.assertIn(field, keys)
        self.assertEqual(metadata["abbreviation"], state_code.lower())

    def testSubsetStateMetadataFields(self):
        """Requesting specific fields in state metadata returns only those
        fields"""
        requested_fields = ["id", "latest_json_date", "latest_json_url",
                            "latest_update"]
        metadata = pyopenstates.get_metadata("OH", fields=requested_fields)
        returned_fields = metadata.keys()

        for field in requested_fields:
            self.assertIn(field, returned_fields)
        for field in returned_fields:
            self.assertIn(field, requested_fields)

    def testDownloadCSV(self):
        """Downloading bulk data on a state in CSV format"""
        zip_file = BytesIO()
        pyopenstates.download_bulk_data("AK", zip_file, data_format="csv")
        zip = ZipFile(zip_file)
        for filename in zip.namelist():
            self.assertTrue(filename.endswith(".csv"))

    def testDownloadJSON(self):
        """Downloading bulk data on a state in JSON format"""
        zip_file = BytesIO()
        pyopenstates.download_bulk_data("AK", zip_file)
        zip = ZipFile(zip_file)
        self.assertIn("metadata.json", zip.namelist())

    def testInvalidState(self):
        """Specifying an invalid state raises a NotFound exception"""
        self.assertRaises(pyopenstates.NotFound, pyopenstates.get_metadata,
                          state="ZZ")

    def testBillSearchFullText(self):
        """A basic full-text search returns results that contain the query
        string"""
        query = "taxi"
        results = pyopenstates.search_bills(state="dc", q=query)
        self.assertGreater(len(results), 1)
        match = False
        for result in results:
            if query.lower() in result["title"].lower():
                match = True
                break
        self.assertTrue(match)

    def testBillDetails(self):
        """Bill details"""
        state = "ca"
        term = "20092010"
        bill_id = "AB 667"
        title = "An act to amend Section 1750.1 of the Business and " \
                "Professions Code, and to amend Section 104830 " \
                "of, and to add Section 104762 to, the Health and Safety " \
                "Code, relating to oral health."

        bill = pyopenstates.get_bill(state=state, term=term, bill_id=bill_id)

        self.assertEqual(bill["bill_id"], bill_id)
        self.assertEqual(bill["title"], title)

    def testBillDetailsByUID(self):
        """Bill details by UID"""
        _id = "CAB00004148"
        title = "An act to amend Section 1750.1 of the Business and " \
                "Professions Code, and to amend Section 104830 " \
                "of, and to add Section 104762 to, the Health and Safety " \
                "Code, relating to oral health."

        bill = pyopenstates.get_bill(_id)

        self.assertEqual(bill["title"], title)

    def testBillDetailInputs(self):
        """Bill detail inputs"""
        state = "ca"
        term = "20092010"
        bill_id = "AB 667"
        _id = "CAB00004148"

        self.assertRaises(ValueError, pyopenstates.get_bill, _id, state, term,
                          bill_id)
        self.assertRaises(ValueError, pyopenstates.get_bill, _id, state)

    def testBillSearchSort(self):
        """Sorting bill search results"""
        sorted_bills = pyopenstates.search_bills(state="dc",
                                                 search_window="term",
                                                 sort="created_at")
        self.assertGreater(sorted_bills[0]["created_at"],
                           sorted_bills[-1]["created_at"])

    def testBillSearchMissingFilter(self):
        """Searching for bills with no filters raises APIError"""
        self.assertRaises(pyopenstates.APIError, pyopenstates.search_bills)

    def testLegislatorSearch(self):
        """Legislator search"""
        state = "dc"
        chamber = "upper"
        results = pyopenstates.search_legislators(state=state, chamber=chamber)
        self.assertGreater(len(results), 2)
        for legislator in results:
            self.assertEqual(legislator["state"], state.lower())
            self.assertEqual(legislator["chamber"], chamber.lower())

    def testLegislatorDetails(self):
        """Legislator details"""
        _id = "DCL000012"
        full_name = "Marion Barry"
        self.assertEqual(pyopenstates.get_legislator(_id)["full_name"],
                         full_name)

    def testLegislatorGeolocation(self):
        """Legislator geolocation"""
        lat = 35.79
        long = -78.78
        state = "nc"
        results = pyopenstates.locate_legislators(lat, long)
        self.assertGreater(len(results), 0)
        for legislator in results:
            self.assertEqual(legislator["state"], state.lower())

    def testCommitteeSearch(self):
        """Committee search"""
        state = "dc"
        results = pyopenstates.search_committees(state=state)
        self.assertGreater(len(results), 2)
        for committee in results:
            self.assertEqual(committee["state"], state.lower())

    def testCommitteeDetails(self):
        """Committee details"""
        _id = "DCC000028"
        comittee = "Transportation and the Environment"
        self.assertEqual(pyopenstates.get_committee(_id)["committee"],
                         comittee)

    def testDistrictSearch(self):
        """District search"""
        state = "nc"
        chamber = "lower"
        results = pyopenstates.search_districts(state=state, chamber=chamber)
        self.assertGreater(len(results), 2)
        for district in results:
            self.assertEqual(district["abbr"], state.lower())
            self.assertEqual(district["chamber"], chamber.lower())

    def testDistrictBoundary(self):
        """District boundary details"""
        boundary_id = "ocd-division/country:us/state:nc/sldl:10"
        _id = "nc-lower-10"
        boundry = pyopenstates.get_district(boundary_id)
        self.assertEqual(boundry["boundary_id"], boundary_id)
        self.assertEqual(boundry["id"], _id)

    def testTimestampConversionInList(self):
        """Timestamp conversion in a list"""
        bill = pyopenstates.search_bills(state="oh")[0]
        self.assertTrue(type(bill["created_at"]) == datetime)

    def testTimestampConversionInDict(self):
        """Timestamp conversion in a dictionary"""
        oh = pyopenstates.get_metadata(state="oh")
        self.assertTrue(type(oh["latest_update"]) == datetime)


if __name__ == "__main__":
    unittest.main(verbosity=2)
