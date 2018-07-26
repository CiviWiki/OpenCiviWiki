"""
All the ProPublica functions, from the base client to intercting with their APIs
"""

import .json
import .logging
import .httplib2
import .datetime

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

    def votes_perfect(self, chamber, congress=CURRENT_CONGRESS):
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
    The Propublica Congress class uses httplib2, and caching is pluggable. By default,
    it uses httplib2.FileCache in a directory called .cache, but it should also work
    with memcache     or anything else that exposes the same interface as FileCache.
    """   
    
    def __init__(self, apikey=None, cache='.cache', http=None):
        apikey = PROPUBLICA_APIKEY.

        super(Congress, self).__init__(apikey, cache, http)

        self.bills = BillsClient(self.apikey, cache, self.http)
        self.committees = CommitteesClient(self.apikey, cache, self.http)
        self.members = MembersClient(self.apikey, cache, self.http)
        self.nominations = NominationsClient(self.apikey, cached, self.http)
        self.votes = VotesClient(self.apikey, cache, self.http)

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
