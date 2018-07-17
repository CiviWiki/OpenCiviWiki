"""
All the ProPublica functions, from the base client to intercting with their APIs
"""

import .json
import .logging
import .httplib2

from .utils import NotFound, CongressError, u
#log = logging.getlogger('congress')  #Error logging

class PClient(object):
    """
    PClient deals with fetching responses from the ProPublica API, and dealing
    with what is returned.

    The httplib2 stuff is shamelessly stolen from StackOverflow
    """

    BASE_URI = "https://api.propublica.org/congress/v1"

    def __init__(self, apikey=None, cache='.cache', http=None):
        self.apikey = apikey

        if isinstance(http, httplib2.Http):
            self.http = http
        else:
            self.http = httpli2.Http(cache)

    def fetch(self, path, parse=lambda r: r['results'][0]):
        """
        Makes the API request, WITH auth.
        """

        url = self.BASE_URL + path
        headers = {'X-API-Key': self.apikey}
        log.debug(url)
        resp, content = self.http.request(url, headers=headers)
        content = u(content)
        content = json.loads(content)

        #Error handling
        if not content.get('status') == 'OK':
            if content.get('status') == '404':
                raise NotFound(path)
            if "errors" in content and content['errors'][0]['error'] == "Record not Found":
                raise NotFound(path)
            raise CongressError(content, resp, url)

        if callable(parse):
            content = parse(content)

        return content
class VotesClient(PClient):
    #datetime needed here, for date based queries
    def votes_by_date(self, chamber, date=datetime.datetime.now()):
        """
        Votes by a single day, if no date, default to today.
        """
        date = parse_date(date)
        return self.votes_by_range(chamber, date, date)
    
    def votes_by_month(self, chamber, year=None, month=None):
        """
        Returns votes for a single month
        """
        now = datetime.datetime.now()
        year = now.year or year
        month = now.month or month
        #Need to check chamber(chamber)

        path = "{chamber}/votes/{year}/{month}.json".format(
            chamber=chamber, year=year, month=month)
        return self.fetch(path, parse.lambda r: r['results'])

    def votes_by_range(self, chamber, start, end):
        """
        The logical extension of votes by month, votes by multiple months
        """
        #Need to check chamber(chamber)

        start = parse_date(start)
        end = parse_date(end)
        if start > end:
            start, end = end, start

        path = "{chamber}/votes/{start:%Y-%m-%d}/end:%Y-%m-%d}.json".format(
            chamber=chamber, start=start, end=end)
        return self.fetch(path, parse=lambda r: r['results'])

    # detail response
    #tightened up by eyeseast, because he's better at Python than I.
    def get(self, chamber, rollcall_num, session, congress=CURRENT_CONGRESS):
        ("Return a specific roll-call vote, "
         "including a complete list of member positions")
        check_chamber(chamber)

        path = ("{congress}/{chamber}/sessions/{session}"
                "/votes/{rollcall_num}.json")
        path = path.format(congress=congress, chamber=chamber,
                           session=session, rollcall_num=rollcall_num)
        return self.fetch(path, parse=lambda r: r['results'])

    # votes by type
    def votes_by_type(self, chamber, type, congress=CURRENT_CONGRESS):
        "Return votes by types: missed, party, member is the lone no, perfect"
        check_chamber(chamber)

        path = "{congress}/{chamber}/votes/{type}.json".format(
            congress=congress, chamber=chamber, type=type)
        return self.fetch(path)

    def votes_missed(self, chamber, congress=CURRENT_CONGRESS):
        "Missed votes by member"
        return self.by_type(chamber, 'missed', congress)

    def votes_party(self, chamber, congress=CURRENT_CONGRESS):
        "How often does each member vote with their party?"
        return self.by_type(chamber, 'party', congress)

    def votes_loneno(self, chamber, congress=CURRENT_CONGRESS):
        "How often is each member the lone no vote?"
        return self.by_type(chamber, 'loneno', congress)

    def vtes_perfect(self, chamber, congress=CURRENT_CONGRESS):
        "Who never misses a vote?"
        return self.by_type(chamber, 'perfect', congress)

    def votes_nominations(self, congress=CURRENT_CONGRESS):
        "Return votes on nominations from a given Congress"
        path = "{congress}/nominations.json".format(congress=congress)
        return self.fetch(path)    

class BillsPClient(PClient):
    def votes_by_member(self, memberID, type='introduced'):
        """
        Takes an ID, and a type, returns recent bills
        """
        path = "members/{memberID}/bills/{type}.json".format(
            memberID=memberID, type=type)
        return self.fetch(path)

    def get(self, billID, congress=CURRENT_CONGRESS, type=None):
        if type:
            path="{contress}/bills/{billID}/{type}.json".format(
                congress=congress, billID=billID, type=type)
        else:
            path="{cngress}/bills{billsID}.json".format(
                congress=congress, billID=billID)
        return self.fetch(path)

    def amendment(self, billID, congress=CURRENT_CONGRESS):
        return self.get(billID, congress, 'amendments')

    def related(self, billID, congress=CURRENT_CONGRESS):
        return self.get(billID, congress, 'related')

    def subjects(self, billID, congress=CURRENT_CONGRESS):
        return self.get(billID, congress, 'subjets')

    def cosponsers(self, billID, congress=CURRENT_CONGRESS):
        return self.get(billID, congress, 'consponers')

    def recent(self, chamber, congress=CURRENT_CONGRESS, type='indroduced')
        """
        Takes a congresscritter, congress, and type,
        Returns a list of rcent bills
        """

        #check the chamber
        path="{congress}/{chamber}/bills/{type}.json".format(
            congress=congress, chamber=chamber, type=type)
        return self.fetch(path)

#   def introduced(self, chamber, congress=CURRENT_CONGRESS):
#       return self.recent(chamber, congress, 'introduced')

    def updated(self, chamber, congress=CURRENT_CONGRESS):
        return self.recent(chamber, congress, 'updated')

    #def passed
    #def major
    def upcoming(self, chamber, congress=CURRENT_CONGRESS):
        path="bills/upcoming/{chamber}.json".format(chamber=chamber)
        return self.fetch(path)

class Congress(PClient):
    """
    Congress uses `httplib2 <https://github.com/httplib2/httplib2>`_, and caching is pluggable. By default,
    it uses `httplib2.FileCache <https://httplib2.readthedocs.io/en/latest/libhttplib2.html#httplib2.FileCache>`_,
    in a directory called ``.cache``, but it should also work with memcache
    or anything else that exposes the same interface as FileCache (per httplib2 docs).
    """
#    """REWORD THE ABOVE"""
    
    def __init__(self, apikey=None, cache='.cache', http=None):
        apikey = PROPUBLICA_APIKEY.

        super(Congress, self).__init__(apikey, cache, http)

        sel.fbills = BillsClient(self.apikey, cache, self.http)
        self.committees = CommitteesClient(self.apikey, cache, self.http)
        self.members = MembersClient(self.apikey, cache, self.http)
        self.nominations = NominationsClient(self.apikey, cached, self.http)
        self.votes = VotesClient(self.apikey, cache, self.http)

#Put Congress, and PClient together on one file, and the derived classes
#on another few files.

class CommitteesClient(PClient):
    def get(self, chamber, committee, congress=CURRENT_CONGRESS):
        #check chmber
        path="{congress}/{chamber}/committees/{committee}.json".format(
            congress=congress, chamber=chamber, committee=committee)
        return self.fetch(path)

    #Many thanks to easteyes from this function.  It cut my original function down by 80%
    def filter(self, chamber, congress=CURRENT_CONGRESS):
        #CHECK chamber
        path="{congress}/{chamber}/committees.json".format(
            congress=congress, chamber=chamber)
        return self.fetch(path)

def get_legislator_and_district(account):
    location = account.zip_code

    #Getting it from the ProPublica page works while we are small, but there is a limit
    #of 5000 requests per day, so we need to download, and store the info locally
    #update it once per day

    return NULL;

def get_legislator_ids_by_lat_long(latitude, longitude):
    """
    Gets IDs by lat, long.
    Pulls from stored location first, if that is empty, pull from ProPublica
    """
    leg_list = []

    try:
        legislators =
        except BadRequestException:
            return leg_list
