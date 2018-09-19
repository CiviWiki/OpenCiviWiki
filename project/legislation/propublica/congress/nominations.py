from .client import Client
from .utils import CURRENT_CONGRESS


class NominationsClient(Client):

    def filter(self, type, congress=CURRENT_CONGRESS):
        path = "{congress}/nominees/{type}.json".format(congress=congress,
                                                        type=type)
        return self.fetch(path)

    def get(self, nominee, congress=CURRENT_CONGRESS):
        path = "{congress}/nominees/{nominee}.json".format(congress=congress,
                                                           nominee=nominee)
        return self.fetch(path)

    def by_state(self, state, congress=CURRENT_CONGRESS):
        path = "{congress}/nominees/state/{state}.json".format(
            congress=congress, state=state)
        return self.fetch(path)
