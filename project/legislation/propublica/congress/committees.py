from .client import Client
from .utils import CURRENT_CONGRESS, check_chamber


class CommitteesClient(Client):

    def filter(self, chamber, congress=CURRENT_CONGRESS):
        check_chamber(chamber)
        path = "{congress}/{chamber}/committees.json".format(
            congress=congress, chamber=chamber)
        return self.fetch(path)

    def get(self, chamber, committee, congress=CURRENT_CONGRESS):
        check_chamber(chamber)
        path = "{congress}/{chamber}/committees/{committee}.json".format(
            congress=congress, chamber=chamber, committee=committee)
        return self.fetch(path)
