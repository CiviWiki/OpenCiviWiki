from .client import Client
from .utils import CURRENT_CONGRESS, check_chamber


class MembersClient(Client):

    def get(self, member_id):
        "Takes a bioguide_id, returns a legislator"
        path = "members/{0}.json".format(member_id)
        return self.fetch(path)

    def filter(self, chamber, congress=CURRENT_CONGRESS, **kwargs):
        """
        Takes a chamber and Congress,
        OR state and district, returning a list of members
        """
        check_chamber(chamber)

        kwargs.update(chamber=chamber, congress=congress)

        if 'state' in kwargs and 'district' in kwargs:
            path = ("members/{chamber}/{state}/{district}/"
                    "current.json").format(**kwargs)

        elif 'state' in kwargs:
            path = ("members/{chamber}/{state}/"
                    "current.json").format(**kwargs)

        else:
            path = ("{congress}/{chamber}/"
                    "members.json").format(**kwargs)

        return self.fetch(path, parse=lambda r: r['results'])

    def bills(self, member_id, type='introduced'):
        "Same as BillsClient.by_member"
        path = "members/{0}/bills/{1}.json".format(member_id, type)
        return self.fetch(path)

    def new(self, **kwargs):
        "Returns a list of new members"
        path = "members/new.json"
        return self.fetch(path)

    def departing(self, chamber, congress=CURRENT_CONGRESS):
        "Takes a chamber and congress and returns a list of departing members"
        check_chamber(chamber)
        path = "{0}/{1}/members/leaving.json".format(congress, chamber)
        return self.fetch(path)

    def compare(self, first, second, chamber, type='votes', congress=CURRENT_CONGRESS):
        """
        See how often two members voted together in a given Congress.
        Takes two member IDs, a chamber and a Congress number.
        """
        check_chamber(chamber)
        path = "members/{first}/{type}/{second}/{congress}/{chamber}.json"
        path = path.format(first=first, second=second, type=type,
                           congress=congress, chamber=chamber)
        return self.fetch(path)

    def party(self):
        "Get state party counts for the current Congress"
        path = "states/members/party.json"
        return self.fetch(path, parse=lambda r: r['results'])
