#!/usr/bin/env python

import datetime
import json
import logging
import os
import time
import urllib
import unittest

import httplib2

from congress import Congress
from congress.utils import CongressError, NotFound, get_congress, u

API_KEY = os.environ['PROPUBLICA_API_KEY']
LOG_LEVEL = getattr(logging, os.environ.get('CONGRESS_LOG_LEVEL', 'INFO').upper(), logging.INFO)

logging.basicConfig(level=LOG_LEVEL)


def close_connections(http):
    for k, conn in http.connections.items():
        conn.close()


class APITest(unittest.TestCase):
    
    def check_response(self, result, url, parse=lambda r: r['results'][0]):
        headers = {'X-API-Key': API_KEY}
        response = self.http.request(url, headers=headers)[1]
        response = u(response)
        response = json.loads(response)
        
        if callable(parse):
            response = parse(response)
        
        self.assertEqual(result, response)
    
    def setUp(self):
        self.congress = Congress(API_KEY)
        self.http = httplib2.Http()

    def tearDown(self):
        close_connections(self.congress.http)
        close_connections(self.http)
    
class MemberTest(APITest):

    def test_get_member(self):
        pelosi = self.congress.members.get('P000197')
        url = "https://api.propublica.org/congress/v1/members/P000197.json"
        self.check_response(pelosi, url)
    
    def test_filter_members(self):
        ri = self.congress.members.filter(chamber='senate', state='RI')
        url = "https://api.propublica.org/congress/v1/members/senate/RI/current.json"
        self.check_response(ri, url, parse=lambda r: r['results'])

        self.assertEqual(len(ri), 2)

    def test_correct_member_counts(self):
        "Check that congress.members.filter returns the right number of members"
        # this may fail if membership changes, because it always gets current members
        states = [
            ('RI', 2),
            ('AL', 7),
            ('AZ', 8),
        ]

        for state, count in states:
            members = self.congress.members.filter(chamber='house', state=state)
            self.assertEqual(len(members), count)
    
    def test_new_members(self):
        new = self.congress.members.new()
        url = "https://api.propublica.org/congress/v1/members/new.json"
        self.check_response(new, url)

    def test_departing_members(self):
        out = self.congress.members.departing(chamber='house', congress=114)
        url = "https://api.propublica.org/congress/v1/114/house/members/leaving.json"
        self.check_response(out, url)
    
    def test_compare_members(self):
        first = "G000575"
        second = "D000624"
        chamber = "house"
        type = "votes"
        congress = 114
        comparison = self.congress.members.compare(first, second, chamber, type, congress)
        url = "https://api.propublica.org/congress/v1/members/G000575/votes/D000624/114/house.json"
        self.check_response(comparison, url)
        

class BillTest(APITest):
    
    def test_recent_bills(self):
        latest = self.congress.bills.recent(chamber='house', congress=114, type='introduced')
        url = "https://api.propublica.org/congress/v1/114/house/bills/introduced.json"
        self.check_response(latest, url)
    
    def test_bills_by_member(self):
        bills = self.congress.bills.by_member('L000287', 'introduced')
        url = "https://api.propublica.org/congress/v1/members/L000287/bills/introduced.json"
        self.check_response(bills, url)
        
    def test_bill_detail(self):
        hr21 = self.congress.bills.get('hr21', 115)
        url = "https://api.propublica.org/congress/v1/115/bills/hr21.json"
        self.check_response(hr21, url)
    
    def test_bill_subjects(self):
        hr2393 = self.congress.bills.subjects('hr2393', 114)
        url = "https://api.propublica.org/congress/v1/114/bills/hr2393/subjects.json"
        self.check_response(hr2393, url)


class CommitteeTest(APITest):
    
    def test_committee_list(self):
        house = self.congress.committees.filter('house', 115)
        url = "https://api.propublica.org/congress/v1/115/house/committees.json"
        self.check_response(house, url)
            
    def test_committee_detail(self):
        HSIG = self.congress.committees.get('house', 'HSIG', 115)
        url = "https://api.propublica.org/congress/v1/115/house/committees/HSIG.json"
        self.check_response(HSIG, url)

class NominationTest(APITest):
    
    def test_nomination_list(self):
        parse = lambda r: r['results'][0]
        received = self.congress.nominations.filter('received', 114)
        url = "https://api.propublica.org/congress/v1/114/nominees/received.json"
        self.check_response(received, url, parse=parse)
        
        withdrawn = self.congress.nominations.filter('withdrawn', 114)
        url = "https://api.propublica.org/congress/v1/114/nominees/withdrawn.json"
        self.check_response(withdrawn, url, parse=parse)

        confirmed = self.congress.nominations.filter('confirmed', 114)
        url = "https://api.propublica.org/congress/v1/114/nominees/confirmed.json"
        self.check_response(confirmed, url, parse=parse)

        updated = self.congress.nominations.filter('updated', 114)
        url = "https://api.propublica.org/congress/v1/114/nominees/updated.json"
        self.check_response(updated, url, parse=parse)
        
    def test_nomination_detail(self):
        pn50 = self.congress.nominations.get('PN40', 115)
        url = "https://api.propublica.org/congress/v1/115/nominees/PN40.json"
        self.check_response(pn50, url)

    def test_nominations(self):
        nom_votes = self.congress.votes.nominations(114)
        url = "https://api.propublica.org/congress/v1/114/nominations.json"
        self.check_response(nom_votes, url)

    def test_nominations_by_state(self):
        parse = lambda r: r['results'][0]
        IL = self.congress.nominations.by_state('IL', 114)
        url = "https://api.propublica.org/congress/v1/114/nominees/state/IL.json"
        self.check_response(IL, url, parse=parse)


class VoteTest(APITest):
    
    def test_votes_by_month(self):
        jan = self.congress.votes.by_month('house', 2016, 1)
        url = "https://api.propublica.org/congress/v1/house/votes/2016/01.json"
        self.check_response(jan, url, parse=lambda r: r['results'])
    
    def test_votes_by_date_range(self):
        sept = self.congress.votes.by_range('house', datetime.date(2010, 9, 1), datetime.date(2010, 9, 30))
        url = "https://api.propublica.org/congress/v1/house/votes/2010-09-1/2010-09-30.json"
        self.check_response(sept, url, parse=lambda r: r['results'])
    
    def test_votes_by_reversed_range(self):
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        self.assertEqual(
            self.congress.votes.by_range('house', today, last_week),
            self.congress.votes.by_range('house', last_week, today)
        )
    
    def test_votes_today(self):
        today = datetime.datetime.today()
        votes = self.congress.votes.today('house')
        url = "https://api.propublica.org/congress/v1/house/votes/{today}/{today}.json".format(
            today=today.strftime('%Y-%m-%d'))

        self.check_response(votes, url, parse=lambda r: r['results'])
    
    def test_votes_by_date(self):
        june14 = datetime.date(2010, 6, 14)
        votes = self.congress.votes.by_date('house', june14)
        url = "https://api.propublica.org/congress/v1/house/votes/2010-06-14/2010-06-14.json"
        self.check_response(votes, url, parse=lambda r: r['results'])
    
    def test_vote_rollcall(self):
        vote = self.congress.votes.get('senate', 17, 2, 114)
        url = "https://api.propublica.org/congress/v1/114/senate/sessions/2/votes/17.json"
        self.check_response(vote, url, parse=lambda r: r['results'])
    
    def test_votes_by_type(self):
        missed = self.congress.votes.by_type('house', 'missed', 114)
        url = "https://api.propublica.org/congress/v1/114/house/votes/missed.json"
        self.check_response(missed, url)
            
    
class ClientTest(APITest):

    def test_generic_fetch(self):
        hr1 = self.congress.bills.get('hr1', 111)
        hr1_generic = self.congress.fetch('111/bills/hr1.json')
        self.assertEqual(hr1, hr1_generic)

class ErrorTest(APITest):
    
    def test_bad_vote_args(self):
        # this needs a chamber argument
        with self.assertRaises(TypeError):
            self.congress.votes.by_month(2010, 11)
    
    def test_no_chamber_args(self):
        # this takes a chamber argument, not a member_id
        with self.assertRaises(TypeError):
            self.congress.bills.introduced('N000032')
    
    def test_404(self):
        # the API returns a 404 for members not found
        with self.assertRaises(NotFound):
            self.congress.members.get('notamember')

class UtilTest(unittest.TestCase):

    def test_congress_years(self):
        
        self.assertEqual(get_congress(1809), 11)
        self.assertEqual(get_congress(1810), 11)
        self.assertEqual(get_congress(2009), 111)
        self.assertEqual(get_congress(2010), 111)

class DjangoTest(unittest.TestCase):
    
    def test_django_cache(self):
        try:
            from django.conf import settings
            settings.configure(CACHE_BACKEND = 'locmem://')
            from django.core.cache import cache
        except ImportError:
            # no Django, so nothing to test
            return
        
        congress = Congress(API_KEY, cache)
        
        self.assertEqual(congress.http.cache, cache)
        self.assertEqual(congress.members.http.cache, cache)
        self.assertEqual(congress.bills.http.cache, cache)
        self.assertEqual(congress.votes.http.cache, cache)
        
        try:
            bills = congress.bills.introduced('house')
        except Exception as e:
            self.fail(e)
        

if __name__ == "__main__":
    unittest.main()
