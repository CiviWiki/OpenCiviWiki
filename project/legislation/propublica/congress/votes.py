import datetime

from .client import Client
from .utils import CURRENT_CONGRESS, check_chamber, parse_date


class VotesClient(Client):

    # date-based queries
    def votes_by_day(self, chamber, date=datetime.datetime.today()):
        """
        Votes cast in a single day, defaults to today.
        """
        date = parse_date(date)
        return self.votes_by_range(chamber, date, date)
    
    def votes_by_month(self, chamber, year=None, month=None):
        """
        Return votes for a single month, defaulting to the current month.
        """
        check_chamber(chamber)

        now = datetime.datetime.now()
        year = year or now.year
        month = month or now.month

        path = "{chamber}/votes/{year}/{month}.json".format(
            chamber=chamber, year=year, month=month)
        return self.fetch(path, parse=lambda r: r['results'])

    def votes_by_range(self, chamber, start, end):
        """
        Return votes cast in a chamber between two dates.
        """
        check_chamber(chamber)

        start, end = parse_date(start), parse_date(end)
        if start > end:
            start = end
            end = start

        path = "{chamber}/votes/{start:%Y-%m-%d}/{end:%Y-%m-%d}.json".format(
            chamber=chamber, start=start, end=end)
        return self.fetch(path, parse=lambda r: r['results'])

    def votes_today(self, chamber):
        "Return today's votes in a given chamber"
        now = datetime.date.today()
        return self.by_range(chamber, now, now)

    # detail response
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
        "Return votes by type: missed, party, lone no, perfect"
        check_chamber(chamber)

        path = "{congress}/{chamber}/votes/{type}.json".format(
            congress=congress, chamber=chamber, type=type)
        return self.fetch(path)

    def votes_missed(self, chamber, congress=CURRENT_CONGRESS):
        "Missed votes by member"
        return self.votes_by_type(chamber, 'missed', congress)

    def votes_with_party(self, chamber, congress=CURRENT_CONGRESS):
        "How often does each member vote with their party?"
        return self.votes_by_type(chamber, 'party', congress)

    def votes_as_lone_no(self, chamber, congress=CURRENT_CONGRESS):
        "How often is each member the lone no vote?"
        return self.votes_by_type(chamber, 'loneno', congress)

    def votes_perfect_record(self, chamber, congress=CURRENT_CONGRESS):
        "Who never misses a vote?"
        return self.votes_by_type(chamber, 'perfect', congress)

    def votes_nominations(self, congress=CURRENT_CONGRESS):
        "Return votes on nominations from a given Congress"
        path = "{congress}/nominations.json".format(congress=congress)
        return self.fetch(path)
